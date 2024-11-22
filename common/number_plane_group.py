from manim import *
from enum import Enum, auto
import re  # 정규표현식 지원 추가


class OriginStyle(Enum):
    DOT = auto()
    CIRCLE = auto()
    CROSS = auto()


class MobjectType(Enum):
    """객체 타입 정의"""
    ORIGIN = auto()
    POINT = auto()
    FUNCTION = auto()
    PARAMETRIC = auto()
    LABEL = auto()


class NumberPlaneGroup(VGroup):
    def __init__(
        self,
        x_range=[-20, 20, 1],
        y_range=[-20, 20, 1],
        x_length=16,
        y_length=16,
        background_line_style={"stroke_opacity": 0.4},
        origin_style_type=OriginStyle.DOT,
        origin_config={
            "color": RED,
            "size": 0.05,
            "opacity": 1.0
        },
        **kwargs
    ):
        super().__init__(**kwargs)

        # NOTE: NumberPlane의 'x_range, y_range'는 생성시에만 설정 가능함.
        #       이 속성들의 변경이 필요하면 새로운 NumberPlane 객체를 생성해야 함.
        self.plane = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            background_line_style=background_line_style
        )
        self.add(self.plane)

        # 원점 저장 (멤버변수 제거)
        origin_marker = self._create_origin_marker(
            origin_style_type,
            origin_config
        )
        self.add(origin_marker)

    def _create_origin_marker(self, style_type, config):
        """원점 표시 생성 헬퍼 메서드"""
        color = config.get("color", RED)
        size = config.get("size", 0.1)
        opacity = config.get("opacity", 1.0)

        # 원점 마커를 plane의 원점 위치에 생성
        origin_point = self.plane.c2p(0, 0)

        if style_type == OriginStyle.DOT:
            marker = Dot(point=origin_point, radius=size,
                         color=color).set_opacity(opacity)
        elif style_type == OriginStyle.CIRCLE:
            marker = Circle(radius=size, color=color,
                            fill_opacity=opacity).move_to(origin_point)
        elif style_type == OriginStyle.CROSS:
            marker = VGroup(
                Line(UP * size, DOWN * size, color=color),
                Line(LEFT * size, RIGHT * size, color=color)
            ).move_to(origin_point).set_opacity(opacity)

        # 메타데이터 설정을 여기서 한 번에 처리
        marker = self._ensure_metadata(marker)
        marker.metadata = {
            "type": MobjectType.ORIGIN,
            "style": style_type
        }

        return marker

    def _ensure_metadata(self, mob):
        """객체에 metadata 속성이 없으면 추가"""
        if not hasattr(mob, "metadata"):
            setattr(mob, "metadata", {})
        return mob

    def _find_mobject(self, name, obj_type=None):
        """이름과 타입으로 객체 찾기"""
        for mob in self.submobjects:
            mob = self._ensure_metadata(mob)
            if (mob.metadata.get("name") == name and
                    (obj_type is None or mob.metadata.get("type") == obj_type)):
                return mob
        return None

    def iter_mobjects(self, name_pattern=None, obj_type=None):
        """이름 패턴과 타입으로 객체들을 필터링하여 이터레이션

        Args:
            name_pattern (str, optional): 정규표현식 패턴 (예: "point_.*", "function_[0-9]+")
            obj_type (str, optional): 객체 타입 (예: "point", "function", "parametric")

        Yields:
            Mobject: 조건에 맞는 객체들
        """
        pattern = re.compile(name_pattern) if name_pattern else None

        for mob in self.submobjects:
            mob = self._ensure_metadata(mob)

            # 타입 체크
            if obj_type and mob.metadata.get("type") != obj_type:
                continue

            # 이름 패턴 체크
            if pattern:
                name = mob.metadata.get("name")
                if not name or not pattern.match(name):
                    continue

            yield mob

    def get_all_points(self):
        """모든 점 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.POINT)

    def get_all_functions(self):
        """모든 함수 그래프 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.FUNCTION)

    def get_all_parametrics(self):
        """모든 파라메트릭 그래프 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.PARAMETRIC)

    def get_all_labels(self):
        """모든 라벨 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.LABEL)

    def remove_all_by_pattern(self, name_pattern, obj_type=None):
        """패턴과 타입에 맞는 모든 객체 제거"""
        for mob in list(self.iter_mobjects(name_pattern, obj_type)):
            self.remove(mob)

    def get_origin_marker(self):
        """원점 마커 가져오기"""
        return self._find_mobject(None, MobjectType.ORIGIN)

    def set_origin_style(self, style_type, config=None):
        """원점 표시 스타일 변경"""
        if config is None:
            config = {
                "color": RED,
                "size": 0.1,
                "opacity": 1.0
            }

        # 기존 원점 표시 제거
        old_marker = self.get_origin_marker()
        if old_marker:
            self.remove(old_marker)

        # 새로운 원점 표시 생성 및 추가
        new_marker = self._create_origin_marker(style_type, config)
        self.add(new_marker)

    def get_current_origin_style(self):
        """현재 원점 스타일 가져오기"""
        marker = self.get_origin_marker()
        return marker.metadata.get("style") if marker else None

    def show_origin(self, show=True):
        marker = self.get_origin_marker()
        if marker:
            marker.set_opacity(1 if show else 0)

    def plot_function(self,
                      func,
                      name=None,
                      x_range=None,
                      color=BLUE,
                      stroke_width=2):
        """함수 그래프 추가"""
        if x_range is None:
            x_range = self.plane.x_range[:2]

        if name is None:
            name = f"function_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.FUNCTION])}"

        graph = self.plane.plot(
            func,
            x_range=x_range,
            color=color,
            stroke_width=stroke_width
        )
        graph = self._ensure_metadata(graph)
        graph.metadata = {"type": MobjectType.FUNCTION, "name": name}

        self.add(graph)
        return graph

    def remove_function(self, name):
        """함수 그래프 제거"""
        graph = self._find_mobject(name, MobjectType.FUNCTION)
        if graph:
            self.remove(graph)

    def get_function_graph(self, name):
        """특정 함수 그래프 가져오기"""
        return self._find_mobject(name, MobjectType.FUNCTION)

    def plot_parametric(self,
                        func,  # (t) -> (x,y) 형태의 함수
                        t_range=[0, 2*PI],
                        name=None,
                        color=BLUE,
                        stroke_width=2):
        """파라메트릭 함수 그래프 추가"""
        if name is None:
            name = f"parametric_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.PARAMETRIC])}"

        graph = self.plane.plot_parametric_curve(
            func,
            t_range=t_range,
            color=color,
            stroke_width=stroke_width
        )
        graph = self._ensure_metadata(graph)
        graph.metadata = {"type": MobjectType.PARAMETRIC, "name": name}

        self.add(graph)
        return graph

    def add_point(self,
                  point,
                  name=None,
                  color=RED,
                  label=None,
                  label_direction=DOWN,
                  label_buff=0.1,
                  font_size=36):
        """점 추가 메서드"""
        if name is None:
            name = f"point_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.POINT])}"

        point_group = VGroup()
        point_group.metadata = {"type": MobjectType.POINT, "name": name}

        dot = Dot(
            point=self.plane.c2p(*point),
            color=color
        )
        point_group.add(dot)

        if label:
            point_label = MathTex(
                label,
                color=color,
                font_size=font_size
            ).next_to(
                dot,
                label_direction,
                buff=label_buff
            )
            point_group.add(point_label)

        self.add(point_group)
        return point_group

    def remove_point(self, name):
        """점 제거"""
        point = self._find_mobject(name, MobjectType.POINT)
        if point:
            self.remove(point)

    def get_point(self, name):
        """특정 점 가져오기"""
        return self._find_mobject(name, MobjectType.POINT)

    def add_label(self,
                  text,
                  position,  # (x,y) 좌표
                  name=None,
                  color=WHITE,
                  font_size=36,
                  tex_template=None,  # LaTeX 템플릿 설정 가능
                  direction=RIGHT,    # 기본 방향
                  buff=0.1):          # 기본 간격
        """임의의 위치에 라벨 추가"""
        if name is None:
            name = f"label_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.LABEL])}"

        # LaTeX 수식 여부에 따라 적절한 객체 생성
        if tex_template:
            label = MathTex(
                text,
                color=color,
                font_size=font_size,
                tex_template=tex_template
            )
        else:
            label = Text(
                text,
                color=color,
                font_size=font_size
            )

        # 좌표계의 위치로 변환
        point = self.plane.c2p(*position)

        # 위치 지정
        label.next_to(point, direction, buff=buff)
        label = self._ensure_metadata(label)
        label.metadata = {"type": MobjectType.LABEL, "name": name}

        self.add(label)
        return label

    def add_tex_label(self,
                      text,
                      position,
                      name=None,
                      color=WHITE,
                      font_size=36,
                      direction=RIGHT,
                      buff=0.1):
        return self.add_label(
            text,
            position,
            name=name,
            color=color,
            font_size=font_size,
            tex_template=TexTemplate(),
            direction=direction,
            buff=buff
        )

    def remove_label(self, name):
        """라벨 제거"""
        label = self._find_mobject(name, MobjectType.LABEL)
        if label:
            self.remove(label)

    def get_label(self, name):
        """특정 라벨 가져오기"""
        return self._find_mobject(name, MobjectType.LABEL)
