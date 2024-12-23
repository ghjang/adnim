from enum import Enum, auto
from manim import *


def calculate_enough_number_of_samples(axes_length):
    """축 길이에 따른 적절한 샘플링 포인트 수 계산"""
    return int(axes_length * config["pixel_width"] / config["frame_width"])


def create_asymptote_lines(axes, discontinuities, color=RED, dash_length=0.1, stroke_width=1.5):
    """탄젠트 함수의 점근선들을 생성

    Args:
        axes: Manim Axes 또는 NumberPlane 객체
        discontinuities: 불연속점들의 x 좌표 리스트
        color: 점근선 색상 (기본값: RED)
        dash_length: 점선의 간격 (기본값: 0.2)
        stroke_width: 선 두께 (기본값: 2)

    Returns:
        VGroup: 생성된 점근선들의 그룹
    """
    return VGroup(*[

        DashedLine(
            start=axes.c2p(x, axes.y_range[0]),
            end=axes.c2p(x, axes.y_range[1]),
            color=color,
            dash_length=dash_length,
            stroke_width=stroke_width
        )
        for x in discontinuities
    ])


class OriginStyle(Enum):
    DOT = auto()
    CIRCLE = auto()
    CROSS = auto()


class MobjectType(Enum):
    """객체 타입 정의"""
    ORIGIN = auto()
    POINT = auto()
    ASYMPTOTES = auto()
    FUNCTION = auto()
    PARAMETRIC = auto()
    LABEL = auto()
    ARC = auto()  # 호 타입 추가
    LINE = auto()  # 선 타입 추가
    POLYGON = auto()  # 다각형 타입 추가
    CIRCLE = auto()  # Circle 타입 추가
    VECTOR = auto()  # 벡터 타입 추가
    RESULTANT_VECTOR = auto()  # 합벡터 타입 추가
    BRACE = auto()  # 브레이스 타입 추가
    BRACE_TEXT = auto()  # 브레이스 텍스트 타입 추가


class NumberPlaneGroupBase(VGroup):
    def __init__(self,
                 x_range=[-20, 20, 1],
                 y_range=[-20, 20, 1],
                 x_length=16,
                 y_length=16,
                 axis_config={},
                 background_line_style={"stroke_opacity": 0.4},
                 origin_config=None,
                 **kwargs):
        super().__init__(**kwargs)
        self._init_called = False  # 중복 초기화 방지

        # 기본 origin_config 설정
        self.default_origin_config = {
            "style": OriginStyle.DOT,
            "color": RED,
            "size": 0.05,
            "opacity": 1.0
        }
        origin_config = origin_config or {}
        self.origin_config = {**self.default_origin_config, **origin_config}

        # 평면 생성
        self.plane = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config=axis_config,
            background_line_style=background_line_style
        )
        self._ensure_metadata(self.plane)
        self.add(self.plane)

        # 원점 마커 생성
        style_type = self.origin_config.pop("style", OriginStyle.DOT)
        origin_marker = self._create_origin_marker(
            style_type, self.origin_config)
        self.add(origin_marker)

        self._ensure_metadata(self)

    def _ensure_single_init(self):
        if not self._init_called:
            self._setup_base()
            self._init_called = True

    def _setup_base(self):
        """공통 초기화 로직"""
        pass

    def _ensure_metadata(self, mob):
        """객체에 metadata 속성이 없으면 추가"""
        if not hasattr(mob, "metadata"):
            setattr(mob, "metadata", {})
        return mob

    def _create_origin_marker(self, style_type, config):
        """원점 표시 생성 헬퍼 메서드"""
        color = config.get("color", RED)
        size = config.get("size", 0.1)
        opacity = config.get("opacity", 1.0)

        # 크기를 좌표계 스케일에 맞게 변환
        origin = self.plane.c2p(0, 0)
        unit_point = self.plane.c2p(size, 0)  # size 만큼의 길이를 가진 점의 좌표
        transformed_size = np.linalg.norm(
            unit_point - origin)  # 실제 화면상의 크기로 변환

        # DOT 타입의 경우 최소 크기 보장
        if (style_type == OriginStyle.DOT):
            marker = Dot(
                point=origin,
                radius=transformed_size,
                color=color,
                stroke_width=2  # stroke_width 추가
            )
            marker.set_stroke(opacity=opacity)  # stroke_opacity 사용
            marker.set_fill(color=color, opacity=opacity)  # fill도 설정
        elif (style_type == OriginStyle.CIRCLE):
            marker = Circle(
                radius=transformed_size,
                color=color,
                fill_opacity=opacity
            ).move_to(origin)
        elif (style_type == OriginStyle.CROSS):
            line1 = Line(UP * transformed_size, DOWN *
                         transformed_size, color=color)
            line2 = Line(LEFT * transformed_size, RIGHT *
                         transformed_size, color=color)
            marker = VGroup(line1, line2)
            marker.move_to(origin)
            # VGroup 전체가 아닌 각 라인에 opacity 설정
            line1.set_stroke(opacity=opacity)
            line2.set_stroke(opacity=opacity)

        # 메타데이터 설정을 여기서 한 번에 처리
        self._ensure_metadata(marker)
        marker.metadata = {
            "type": MobjectType.ORIGIN,
            "style": style_type
        }

        return marker

    def _copy_origin_marker(self, new_group):
        """원점 마커를 새로운 좌표계에 맞게 복사"""
        origin_marker = self.get_origin_marker()
        if not origin_marker:
            return

        # 기존 원점의 스타일과 속성을 가져옴
        style_type = origin_marker.metadata.get("style")

        # 타입별로 색상과 opacity 가져오기
        if style_type == OriginStyle.CROSS:
            color = origin_marker[0].get_color()  # 첫 번째 라인의 색상만 사용
            opacity = origin_marker[0].stroke_opacity
            old_size = abs(origin_marker[0].get_length()) / 2
        elif style_type == OriginStyle.DOT:
            color = origin_marker.get_color()
            opacity = origin_marker.get_fill_opacity()  # fill_opacity 사용

            # NOTE: DOT의 경우 최소 크기 보장시킴.
            #       'scale-down'되는 경우 너무 작아지면
            #       원점이 아예 보이지 않아서 일단 적당한 값의 최소값으로 표시하도록 함.
            MIN_DOT_SIZE = 0.065
            old_size = max(origin_marker.radius, MIN_DOT_SIZE)
        else:  # CIRCLE
            color = origin_marker.get_color()
            opacity = origin_marker.get_opacity()
            old_size = abs(origin_marker.get_width()) / 2

        # 크기 스케일 계산 (x축 기준)
        old_unit = abs(self.plane.c2p(1, 0)[0] - self.plane.c2p(0, 0)[0])
        new_unit = abs(new_group.plane.c2p(1, 0)[
                       0] - new_group.plane.c2p(0, 0)[0])
        new_size = old_size * (new_unit / old_unit)

        # 새로운 원점 스타일 설정
        new_group.set_origin_style(
            style_type,
            {
                "color": color,
                "size": new_size,
                "opacity": opacity
            }
        )

    def _get_unit_length(self):
        """현재 좌표계의 단위 길이 계산"""
        origin = self.plane.c2p(0, 0)
        unit_point = self.plane.c2p(1, 0)
        return np.linalg.norm(unit_point - origin)

    def _transform_unit_length(self, length, source_plane=None):
        """단위 길이를 화면 좌표계로 변환"""
        source_plane = source_plane or self.plane
        origin = source_plane.c2p(0, 0)
        unit_point = source_plane.c2p(length, 0)
        return np.linalg.norm(unit_point - origin)

    def _transform_point(self, point, source_plane=None):
        """점 좌표를 화면 좌표계로 변환"""
        source_plane = source_plane or self.plane
        if isinstance(point, (tuple, list, np.ndarray)):
            return source_plane.c2p(*point)
        return point

    def _calculate_relative_radius(self, circle, source_plane, target_plane):
        """원의 상대적 반지름 계산"""
        # 원본 좌표계의 단위 길이
        source_unit = np.linalg.norm(
            source_plane.c2p(1, 0) - source_plane.c2p(0, 0))
        # 대상 좌표계의 단위 길이
        target_unit = np.linalg.norm(
            target_plane.c2p(1, 0) - target_plane.c2p(0, 0))

        # 원의 화면상 반지름을 논리적 단위로 변환
        return (circle.radius / source_unit)

    def _copy_mobjects_with_transform(self, new_group):
        """객체 복사 및 변환 로직 분리"""
        for mob in self.submobjects:
            if not hasattr(mob, 'metadata'):
                continue

            mob_type = mob.metadata.get('type')
            if mob_type == MobjectType.CIRCLE:
                # 원의 경우, 좌표계의 단위 길이를 고려하여 처리
                center = self.plane.p2c(mob.get_center())
                # 상대적 반지름 계산
                logical_radius = self._calculate_relative_radius(
                    mob, self.plane, new_group.plane)

                new_group.add_circle(
                    center_point=center,
                    radius=logical_radius,
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    fill_opacity=mob.fill_opacity,
                    stroke_width=mob.stroke_width,
                    stroke_opacity=mob.stroke_opacity
                )
            elif mob_type == MobjectType.VECTOR:
                # 벡터 복사 시 메타데이터 보존
                start_point = self.plane.p2c(mob.get_start())
                end_point = self.plane.p2c(mob.get_end())
                relative_vec = (
                    end_point[0] - start_point[0],
                    end_point[1] - start_point[1]
                )
                new_group.add_vector(
                    vec=relative_vec,
                    name=mob.metadata.get('name'),
                    color=mob.get_color(),
                    stroke_width=mob.stroke_width,
                    max_tip_length_to_length_ratio=mob.max_tip_length_to_length_ratio,
                    tip_length=mob.tip_length,
                    start_point=start_point
                )
            elif mob.metadata.get("type") == MobjectType.POINT:
                new_point = new_group.add_point(
                    self.plane.p2c(mob.get_center()),
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    radius=mob.radius
                )
                if len(mob.submobjects) > 1:
                    new_point_label = new_point[1]
                    new_point_label.move_to(new_group.plane.c2p(
                        *self.plane.p2c(mob.submobjects[1].get_center())))
            elif mob.metadata.get("type") == MobjectType.ASYMPTOTES:
                # TODO: 점근선 객체 복사
                pass
            elif mob.metadata.get("type") == MobjectType.FUNCTION:
                new_group.plot_function(
                    lambda x: self.plane.p2c(mob.underlying_function(x))[1],
                    name=mob.metadata.get("name"),
                    x_range=mob.metadata.get("x_range"),
                    color=mob.get_color(),
                    stroke_width=mob.stroke_width
                )
            elif mob.metadata.get("type") == MobjectType.PARAMETRIC:
                new_group.plot_parametric(
                    lambda t: self.plane.p2c(mob.underlying_function(t)),
                    t_range=mob.metadata.get("t_range"),
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    stroke_width=mob.stroke_width
                )
            elif mob.metadata.get("type") == MobjectType.LABEL:
                new_group.add_label(
                    mob.get_tex_string(),
                    self.plane.p2c(mob.get_center()),
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    font_size=mob.font_size
                )
            elif mob.metadata.get("type") == MobjectType.ARC:
                new_group.add_arc(
                    self.plane.p2c(mob.arc_center),
                    radius=mob.radius,
                    start_angle=mob.start_angle,
                    angle=mob.angle,
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    stroke_width=mob.stroke_width,
                    dash_length=mob.dash_length
                )
            elif mob.metadata.get("type") == MobjectType.LINE:
                new_group.add_line(
                    self.plane.p2c(mob.get_start()),
                    self.plane.p2c(mob.get_end()),
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    stroke_width=mob.stroke_width
                )
            elif mob.metadata.get("type") == MobjectType.POLYGON:
                new_group.add_polygon(
                    [self.plane.p2c(p) for p in mob.get_vertices()],
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    fill_opacity=mob.fill_opacity,
                    stroke_width=mob.stroke_width
                )
            elif mob.metadata.get("type") == MobjectType.CIRCLE:
                # 원의 경우, 좌표계의 단위 길이를 고려하여 처리
                center = self.plane.p2c(mob.get_center())
                # 원본 원의 실제 반지름을 논리적 단위로 변환
                logical_radius = mob.radius / old_unit_length   # FIXME: old_unit_length가 정의되지 않음

                new_group.add_circle(
                    center_point=center,
                    radius=logical_radius,  # 논리적 단위의 반지름 사용
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    fill_opacity=mob.fill_opacity,
                    stroke_width=mob.stroke_width,
                    stroke_opacity=mob.stroke_opacity
                )
            elif mob.metadata.get("type") == MobjectType.BRACE:
                # TODO: Brace 객체 복사
                pass
            elif mob.metadata.get("type") == MobjectType.BRACE_TEXT:
                # TODO: Brace Text 객체 복사
                pass
