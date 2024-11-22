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
    ARC = auto()  # 호 타입 추가
    LINE = auto()  # 선 타입 추가
    POLYGON = auto()  # 다각형 타입 추가


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
        self._ensure_metadata(self.plane)
        self.add(self.plane)

        # 원점 저장 (멤버변수 제거)
        origin_marker = self._create_origin_marker(
            origin_style_type,
            origin_config
        )
        self.add(origin_marker)

        self._ensure_metadata(self)

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

    def _find_mobject(self, name, obj_type=None):
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
        graph.metadata = {"type": MobjectType.FUNCTION, "name": name}

        self.add(graph)
        return graph

    def remove_function(self, name):
        """함수 그래프 제거"""
        graph = self._find_mobject(name, MobjectType.FUNCTION)
        if (graph):
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
        point = self._find_mobject(name, MobjectType.POINT)
        if (point):
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
        label = self._find_mobject(name, MobjectType.LABEL)
        if (label):
            self.remove(label)

    def get_label(self, name):
        """특정 라벨 가져오기"""
        return self._find_mobject(name, MobjectType.LABEL)

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

    def add_equal_marks(self, start_point, end_point, num_marks=1, size=0.15, color=BLUE, spacing_ratio=0.05):
        """선분에 같음을 나타내는 마크를 추가합니다."""
        # 시작점과 끝점을 화면 좌표계로 변환
        start = np.array(self.plane.c2p(*start_point))
        end = np.array(self.plane.c2p(*end_point))

        # 선분의 방향 벡터와 중심점
        line_vector = end - start
        line_length = np.linalg.norm(line_vector)
        center = (start + end) / 2

        # 마커들 사이의 간격
        spacing = line_length * spacing_ratio

        # 첫 마커의 위치 계산 (마커 그룹의 중심이 선분의 중심과 일치하도록)
        if num_marks % 2 == 0:  # 짝수 개의 마커
            offset = spacing / 2
            positions = np.linspace(-offset * (num_marks - 1),
                                    offset * (num_marks - 1), num_marks)
        else:  # 홀수 개의 마커
            positions = np.linspace(-spacing * (num_marks - 1)/2,
                                    spacing * (num_marks - 1)/2, num_marks)

        # 선분에 수직인 단위 벡터 계산
        perpendicular = np.array([-line_vector[1], line_vector[0], 0])
        perpendicular = perpendicular / np.linalg.norm(perpendicular)

        marks = VGroup()

        # 각 위치에 마커 생성
        for pos in positions:
            mark_center = center + pos * line_vector / line_length
            mark = Line(
                mark_center - size/2 * perpendicular,
                mark_center + size/2 * perpendicular,
                color=color
            )
            marks.add(mark)

        self.add(marks)
        return marks

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

    def add_angle_mark(self,
                       point1,
                       point2,
                       point3,
                       radius=0.3,
                       color=WHITE,
                       other_angle=False):
        """세 점으로 정의되는 각도를 표시합니다.
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

    def add_equal_angle_marks(self,
                              angle_point,
                              start_angle=0,
                              angle=PI/6,
                              radius=0.3,
                              mark_size=0.15,
                              color=LIGHT_BROWN,
                              num_marks=1,
                              spacing=0.05,
                              name=None):
        """각도가 같음을 표시하는 작은 마커를 추가합니다."""
        if name is None:
            name = f"equal_angle_mark_{len([m for m in self.submobjects if getattr(m, 'metadata', {}).get('type') == 'EQUAL_ANGLE_MARK'])}"

        marks = VGroup()
        marks.metadata = {}

        for i in range(num_marks):
            # 각 마크의 반지름 계산
            r = radius + (i * spacing)

            # 호의 중간 각도 계산 (실제 호의 중간점)
            mid_angle = start_angle + angle/2

            # 호의 중간 지점 계산
            mid_point = np.array([
                r * np.cos(mid_angle),
                r * np.sin(mid_angle),
                0
            ])

            # 접선 벡터 계산 (호의 접선 방향)
            tangent = np.array([
                -mid_point[1],  # -y
                mid_point[0],   # x
                0
            ])
            tangent = tangent / np.linalg.norm(tangent)  # 정규화

            # 마커의 시작점과 끝점 계산
            mark_start = mid_point - tangent * mark_size/2
            mark_end = mid_point + tangent * mark_size/2

            # 마커를 각의 꼭지점 위치로 이동
            mark = Line(
                self.plane.c2p(*angle_point) + mark_start,
                self.plane.c2p(*angle_point) + mark_end,
                color=color
            )

            # 메타데이터 설정
            self._ensure_metadata(mark)
            mark.metadata = {
                "type": "EQUAL_ANGLE_MARK_LINE",
                "parent": name,
                "index": i
            }
            marks.add(mark)

        # VGroup의 메타데이터 설정
        marks.metadata = {
            "type": "EQUAL_ANGLE_MARK",
            "name": name
        }

        self.add(marks)
        return marks
