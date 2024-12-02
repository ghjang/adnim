from manim import *
from enum import Enum, auto
import re  # 정규표현식 지원 추가
from .angle_decoration import AngleMarker  # AngleMarker 클래스 임포트
from .line_decoration import LineMarker  # LineMarker 클래스 임포트
from .rotate_vector import VECTOR_STYLE  # VECTOR_STYLE 임포트 추가


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
    ARC = auto()  # 호 타입 추가
    LINE = auto()  # 선 타입 추가
    POLYGON = auto()  # 다각형 타입 추가
    CIRCLE = auto()  # Circle 타입 추가
    VECTOR = auto()  # 벡터 타입 추가


class NumberPlaneGroup(VGroup):
    def __init__(self, x_range=[-20, 20, 1], y_range=[-20, 20, 1],
                 x_length=16, y_length=16,
                 background_line_style={"stroke_opacity": 0.4},
                 origin_config=None,
                 **kwargs):
        super().__init__(**kwargs)

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

    def _ensure_metadata(self, mob):
        """객체에 metadata 속성이 없으면 추가"""
        if not hasattr(mob, "metadata"):
            setattr(mob, "metadata", {})
        return mob

    def find_mobject(self, name, obj_type=None):
        """이름과 타입으로 객체 찾기"""
        for mob in self.submobjects:
            self._ensure_metadata(mob)
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
            self._ensure_metadata(mob)

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
        return self.find_mobject(None, MobjectType.ORIGIN)

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
        if (old_marker):
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
        if (marker):
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
        self._ensure_metadata(graph)
        graph.metadata = {
            "type": MobjectType.FUNCTION,
            "name": name,
            "base_plane": self.plane,  # 기준 평면 저장
            "x_range": x_range         # x_range 저장
        }

        self.add(graph)
        return graph

    def remove_function(self, name):
        """함수 그래프 제거"""
        graph = self.find_mobject(name, MobjectType.FUNCTION)
        if (graph):
            self.remove(graph)

    def get_function_graph(self, name):
        """특정 함수 그래프 가져오기"""
        return self.find_mobject(name, MobjectType.FUNCTION)

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
        self._ensure_metadata(graph)
        graph.metadata = {"type": MobjectType.PARAMETRIC, "name": name}

        self.add(graph)
        return graph

    def add_point(self,
                  point,
                  name=None,
                  color=RED,
                  radius=DEFAULT_DOT_RADIUS,
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
            radius=radius,  # radius 적용
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
        point = self.find_mobject(name, MobjectType.POINT)
        if (point):
            self.remove(point)

    def get_point(self, name):
        """특정 점 가져오기"""
        return self.find_mobject(name, MobjectType.POINT)

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
        self._ensure_metadata(label)
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
        label = self.find_mobject(name, MobjectType.LABEL)
        if (label):
            self.remove(label)

    def get_label(self, name):
        """특정 라벨 가져오기"""
        return self.find_mobject(name, MobjectType.LABEL)

    def add_arc(self,
                center_point,  # 중심점 좌표 (x,y)
                radius=1,
                start_angle=0,
                angle=TAU/4,
                name=None,
                color=BLUE,
                stroke_width=2,
                dash_length=None):  # None이면 실선, 값이 있으면 점선
        """호 추가 메서드"""
        if name is None:
            name = f"arc_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.ARC])}"

        # 중심점 좌표 변환
        arc_center = self.plane.c2p(*center_point)

        # 반지름을 화면 좌표계로 변환 (x축 기준으로 변환)
        radius_point = self.plane.c2p(
            center_point[0] + radius, center_point[1]
        )
        transformed_radius = np.linalg.norm(radius_point - arc_center)

        # 호 객체 생성
        arc = Arc(
            radius=transformed_radius,  # 변환된 반지름 사용
            start_angle=start_angle,
            angle=angle,
            arc_center=arc_center,
            stroke_width=stroke_width,
            color=color
        )

        # 점선 설정
        if dash_length is not None:
            arc = DashedVMobject(
                arc,
                num_dashes=int(radius * 4),
                dashed_ratio=0.5  # 선과 공백의 비율
            )

        # 메타데이터 설정
        self._ensure_metadata(arc)
        arc.metadata = {"type": MobjectType.ARC, "name": name}

        self.add(arc)
        return arc

    def add_line(self,
                 start_point,  # (x1, y1) 좌표
                 end_point,    # (x2, y2) 좌표
                 name=None,
                 color=BLUE,
                 stroke_width=2):
        """선 추가 메서드"""
        if name is None:
            name = f"line_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.LINE])}"

        # 시작점과 끝점의 좌표를 변환
        start = self.plane.c2p(*start_point)
        end = self.plane.c2p(*end_point)

        # 선 객체 생성
        line = Line(
            start=start,
            end=end,
            color=color,
            stroke_width=stroke_width
        )

        # 메타데이터 설정
        self._ensure_metadata(line)
        line.metadata = {"type": MobjectType.LINE, "name": name}

        self.add(line)
        return line

    def add_polygon(self,
                    points,        # [(x1,y1), (x2,y2), ...] 좌표 리스트
                    name=None,
                    color=BLUE,
                    fill_opacity=0.2,
                    stroke_width=2):
        """다각형 추가 메서드"""
        if name is None:
            name = f"polygon_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.POLYGON])}"

        # 좌표들을 화면 좌표계로 변환
        vertices = [self.plane.c2p(*point) for point in points]

        # 다각형 객체 생성
        polygon = Polygon(
            *vertices,
            color=color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width
        )

        # 메타데이터 설정
        self._ensure_metadata(polygon)
        polygon.metadata = {"type": MobjectType.POLYGON, "name": name}

        self.add(polygon)
        return polygon

    def add_triangle(self,
                     p1, p2, p3,  # 세 점의 좌표 (x,y)
                     name=None,
                     color=BLUE,
                     fill_opacity=0.2,
                     stroke_width=2):
        """삼각형 추가 메서드"""
        if name is None:
            name = f"triangle_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.POLYGON])}"

        # 좌표들을 화면 좌표계로 변환
        vertices = [self.plane.c2p(*p) for p in [p1, p2, p3]]

        # Triangle 클래스 직접 사용
        triangle = Triangle(
            color=color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width
        )
        triangle.set_points_as_corners(
            [*vertices, vertices[0]])  # 마지막 점을 처음으로 연결

        # 메타데이터 설정
        self._ensure_metadata(triangle)
        triangle.metadata = {"type": MobjectType.POLYGON, "name": name}

        self.add(triangle)
        return triangle

    def add_regular_polygon(self,
                            n_sides,         # 변의 수
                            center_point,    # 중심점 (x,y)
                            radius=1,        # 외접원 반지름
                            name=None,
                            color=BLUE,
                            fill_opacity=0.2,
                            stroke_width=2,
                            start_angle=0):  # 시작 각도
        """정다각형 추가 메서드"""
        if name is None:
            name = f"regular_polygon_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.POLYGON])}"

        # 중심점 좌표 변환
        center = self.plane.c2p(*center_point)

        # 반지름 변환
        radius_point = self.plane.c2p(
            center_point[0] + radius, center_point[1])
        transformed_radius = np.linalg.norm(radius_point - center)

        # 정다각형 객체 생성
        polygon = RegularPolygon(
            n=n_sides,
            start_angle=start_angle,
            radius=transformed_radius,
            color=color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width
        ).move_to(center)

        # 메타데이터 설정
        self._ensure_metadata(polygon)
        polygon.metadata = {"type": MobjectType.POLYGON, "name": name}

        self.add(polygon)
        return polygon

    def add_regular_triangle(self,
                             center_point,
                             radius=1,
                             name=None,
                             color=BLUE,
                             fill_opacity=0.2,
                             stroke_width=2,
                             start_angle=0):
        """정삼각형 추가 메서드"""
        if name is None:
            name = f"regular_triangle_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.POLYGON])}"

        # 중심점과 반지름 변환
        center = self.plane.c2p(*center_point)
        radius_point = self.plane.c2p(
            center_point[0] + radius, center_point[1])
        transformed_radius = np.linalg.norm(radius_point - center)

        # RegularPolygon 클래스로 정삼각형 생성 (n=3)
        triangle = RegularPolygon(
            n=3,
            radius=transformed_radius,
            start_angle=start_angle,
            color=color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width
        ).move_to(center)

        # 메타데이터 설정
        self._ensure_metadata(triangle)
        triangle.metadata = {"type": MobjectType.POLYGON, "name": name}

        self.add(triangle)
        return triangle

    def add_circle(self,
                   center_point,  # 중심점 좌표 (x,y)
                   radius=1,
                   name=None,
                   color=BLUE,
                   fill_opacity=0.2,
                   stroke_width=2,
                   stroke_opacity=1.0):  # stroke_opacity 파라미터 추가
        """원 추가 메서드"""
        if name is None:
            name = f"circle_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.CIRCLE])}"

        # 중심점 좌표 변환
        center = self.plane.c2p(*center_point)

        # 반지름을 화면 좌표계로 변환 (x축 기준으로 변환)
        radius_point = self.plane.c2p(
            center_point[0] + radius, center_point[1]
        )
        transformed_radius = np.linalg.norm(radius_point - center)

        # Circle 객체 생성
        circle = Circle(
            radius=transformed_radius,
            color=color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity  # 선 투명도 적용
        ).move_to(center)

        # 메타데이터 설정
        self._ensure_metadata(circle)
        circle.metadata = {"type": MobjectType.CIRCLE, "name": name}

        self.add(circle)
        return circle

    def add_line_marker(self,
                        start_point,
                        end_point,
                        num_marks=1,
                        size=0.15,
                        color=BLUE,
                        spacing=0.1,
                        stroke_width=2):
        """선분에 같음을 나타내는 마커를 추가한다."""
        # 시작점과 끝점을 화면 좌표계로 변환하여 Line 객체 생성
        start = self.plane.c2p(*start_point)
        end = self.plane.c2p(*end_point)
        line = Line(start, end)

        markers = LineMarker(
            line,
            length=size,
            color=color,
            count=num_marks,
            spacing=spacing,
            stroke_width=stroke_width
        )

        self.add(markers)
        return markers

    def add_right_angle_mark(self,
                             corner_point,
                             direction1=RIGHT*0.5,
                             direction2=UP*0.5,
                             size=0.2,
                             color=LIGHT_BROWN):
        """직각을 표시하는 기호를 추가합니다."""
        # 코너 포인트를 화면 좌표계로 변환
        corner = self.plane.c2p(*corner_point)

        # 두 선분 생성
        line1 = Line(corner, corner + direction1)
        line2 = Line(corner, corner + direction2)

        # RightAngle 클래스 사용
        angle_mark = RightAngle(
            line1, line2,
            length=size,
            color=color
        )

        self._ensure_metadata(angle_mark)
        angle_mark.metadata = {"type": "ANGLE_MARK"}

        self.add(angle_mark)
        return angle_mark

    def add_angle(self,
                  point1,
                  point2,
                  point3,
                  radius=0.3,
                  color=WHITE,
                  other_angle=False):
        """세 점으로 정의되는 각도를 표시한다.
        Args:
            point1, point2, point3: 각을 이루는 세 점의 좌표 (시계방향)
                point2가 각의 꼭지점
            radius: 각도 표시의 크기
            color: 각도 표시의 색상
            other_angle: True이면 큰 각을 표시, False이면 작은 각을 표시
        """
        # 좌표를 화면 좌표계로 변환
        p1 = self.plane.c2p(*point1)
        p2 = self.plane.c2p(*point2)
        p3 = self.plane.c2p(*point3)

        # Angle 객체 생성
        angle = Angle(
            Line(p2, p1), Line(p2, p3),
            radius=radius,
            color=color,
            other_angle=other_angle
        )

        # 메타데이터 설정
        self._ensure_metadata(angle)
        angle.metadata = {"type": "ANGLE_MARK"}

        self.add(angle)
        return angle

    def add_angle_marker(
        self,
        angle: Angle,  # Angle 객체를 직접 받도록 수정
        mark_size=0.15,
        color=LIGHT_BROWN,
        num_marks=1,
        spacing=0.1,
        stroke_width=2,
        name=None
    ):
        """각도가 같음을 표시하는 작은 마커를 추가한다."""
        marker = AngleMarker(
            angle,
            length=mark_size,
            color=color,
            count=num_marks,
            spacing=spacing,
            stroke_width=stroke_width
        )

        self.add(marker)
        return marker

    def add_vector(self, vec, name=None, color=RED, start_point=None, **kwargs):
        """벡터 추가 메서드 개선"""
        if name is None:
            name = f"vector_{len(list(self.iter_mobjects(obj_type=MobjectType.VECTOR)))}"

        # 시작점 처리
        if start_point is None:
            start_point = (0, 0)

        # 시작점과 벡터 좌표 변환
        start = self._transform_point(start_point)
        end = self._transform_point((
            start_point[0] + vec[0],
            start_point[1] + vec[1]
        ))

        # 표준 벡터 스타일과 사용자 정의 스타일 병합
        vector_style = {**VECTOR_STYLE, **kwargs}
        
        # 벡터 생성
        vector = Vector(
            direction=end - start,
            color=color,
            **vector_style
        ).shift(start)

        # 메타데이터 설정
        self._ensure_metadata(vector)
        vector.metadata.update({
            "type": MobjectType.VECTOR,
            "name": name,
            "coordinates": vec,
            "start_point": start_point,
            "style": vector_style  # 스타일 정보도 저장
        })

        self.add(vector)
        return vector

    def _copy_origin_marker(self, new_group):
        """원점 마���를 새로운 좌표계에 맞게 복사"""
        origin_marker = self.get_origin_marker()
        if not origin_marker:
            return

        # 기존 원점의 스타일과 속성을 가져옴
        style_type = origin_marker.metadata.get("style")

        # 타입별로 색상과 opacity 가져오기
        if style_type == OriginStyle.CROSS:
            color = origin_marker[0].get_color()  # 첫 번째 라인의 색상만 ���용
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

    def copy_with_transformed_plane(self, x_range=None, y_range=None,
                                    x_length=None, y_length=None, **kwargs):
        """좌표계 변환 복사 메서드 개선"""
        new_group = super().copy()
        new_group.submobjects.clear()  # 기존 submobjects 제거

        # background_line_style이 명시적으로 지정되지 않은 경우 원본의 스타일을 사용
        if 'background_line_style' not in kwargs:
            kwargs['background_line_style'] = self.plane.background_line_style

        # 새로운 평면 생성
        new_plane = NumberPlane(
            x_range=x_range or self.plane.x_range,
            y_range=y_range or self.plane.y_range,
            x_length=x_length or self.plane.x_length,
            y_length=y_length or self.plane.y_length,
            **kwargs
        )

        # 메타데이터 보존
        new_group._ensure_metadata(new_plane)
        new_group.plane = new_plane
        new_group.add(new_plane)

        # 원점 마커 복사
        self._copy_origin_marker(new_group)

        # 다른 객체들 복사
        self._copy_mobjects_with_transform(new_group)

        return new_group

    def _get_unit_length(self):
        """현재 좌표계의 단위 길이 계산"""
        origin = self.plane.c2p(0, 0)
        unit_point = self.plane.c2p(1, 0)
        return np.linalg.norm(unit_point - origin)

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
                logical_radius = mob.radius / old_unit_length

                new_group.add_circle(
                    center_point=center,
                    radius=logical_radius,  # 논리적 단위의 반지름 사용
                    name=mob.metadata.get("name"),
                    color=mob.get_color(),
                    fill_opacity=mob.fill_opacity,
                    stroke_width=mob.stroke_width,
                    stroke_opacity=mob.stroke_opacity
                )
