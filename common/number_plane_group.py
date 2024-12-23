import re  # 정규표현식 지원 추가
from manim import *

from .number_plane_group_impl.number_plane_group_base import (
    calculate_enough_number_of_samples,
    create_asymptote_lines,
    MobjectType,
    OriginStyle,
    NumberPlaneGroupBase
)

from .angle_decoration import AngleMarker  # AngleMarker 클래스 임포트
from .line_decoration import LineMarker  # LineMarker 클래스 임포트
from .rotate_vector import VECTOR_STYLE  # VECTOR_STYLE 임포트 추가


class NumberPlaneGroup(NumberPlaneGroupBase):
    def __init__(self,
                 x_range=[-20, 20, 1],
                 y_range=[-20, 20, 1],
                 x_length=16,
                 y_length=16,
                 axis_config={},
                 background_line_style={"stroke_opacity": 0.4},
                 origin_config=None,
                 **kwargs):
        all_params = {
            'x_range': x_range,
            'y_range': y_range,
            'x_length': x_length,
            'y_length': y_length,
            'axis_config': axis_config,
            'background_line_style': background_line_style,
            'origin_config': origin_config,
            **kwargs
        }
        super().__init__(**all_params)

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
                      stroke_width=2,
                      **kwargs):  # 추가 인자를 받을 수 있도록 kwargs 추가
        """함수 그래프 추가"""
        if x_range is None:
            x_range = self.plane.x_range[:2]

        if name is None:
            name = f"function_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.FUNCTION])}"

        graph = self.plane.plot(
            func,
            x_range=x_range,
            color=color,
            stroke_width=stroke_width,
            **kwargs  # 추가 인자들을 plot 메서드로 전달
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

    def plot_discontinuous_function(
        self,
        func,                    # 실제 함수 (x -> y)
        x_range=None,           # x 범위
        # (x_min, x_max) -> [x1, x2, ...] 불연속점 계산 함수
        discontinuity_finder=None,
        epsilon=0.001,          # 불연속점 근처 제외 범위
        y_limit=None,           # y값 제한 (None이면 axes의 y범위 사용)
        y_margin_ratio=0.17,    # y축 범위에 대한 여유 공간 비율
        name=None,  # 이름 파라미터 추가
        color=BLUE,
        stroke_width=2,
        show_discontinuities=True,  # 불연속점 표시 여부
        discontinuity_config=None,  # 점근선 스타일 설정
        **kwargs
    ):
        """불연속 구간을 포함하는 함수 그래프 추가

        Args:
            func: 그릴 함수 (x -> y)
            x_range: x 범위. None이면 plane의 x_range 사용
            discontinuity_finder: 불연속점을 찾는 함수 (x_min, x_max) -> [불연속점들]
            epsilon: 불연속점 근처에서 제외할 범위
            y_limit: y값 제한
            y_margin_ratio: y축 범위에 대한 여유 공간 비율
            color: 그래프 색상
            stroke_width: 선 두께
            show_discontinuities: 불연속점 표시 여부
            discontinuity_config: 점근선 설정 (color, dash_length, stroke_width 등)
            **kwargs: plot_function에 전달할 추가 인자

        Returns:
            VGroup: (graph_segments, discontinuity_lines)
        """
        if x_range is None:
            x_range = self.plane.x_range[:2]

        if name is None:
            name = f"discontinuous_function_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.FUNCTION])}"

        if discontinuity_config is None:
            discontinuity_config = {
                "color": RED,
                "dash_length": 0.1,
                "stroke_width": 1.5
            }

        # 불연속점이 없으면 일반 plot_function 사용
        if discontinuity_finder is None:
            return self.plot_function(
                func,
                x_range=x_range,
                color=color,
                stroke_width=stroke_width,
                **kwargs
            )

        # 불연속점과 연속구간 계산
        discontinuities = discontinuity_finder(x_range[0], x_range[1])

        # 연속구간 계산
        ranges = []
        current = x_range[0]

        for x in discontinuities:
            if current < x - epsilon:
                ranges.append((current, x - epsilon))
            current = x + epsilon

        if current < x_range[1]:
            ranges.append((current, x_range[1]))

        # y값 제한 계산
        if y_limit is None:
            y_limit = max(abs(self.plane.y_range[0]), abs(
                self.plane.y_range[1]))
            y_margin = y_limit * y_margin_ratio
            y_limit += y_margin

        # 그래프 세그먼트 생성
        result_group = VGroup()

        # 메타데이터 설정
        self._ensure_metadata(result_group)
        result_group.metadata = {
            "type": MobjectType.FUNCTION,
            "name": name,
            "base_plane": self.plane,
            "x_range": x_range,
            "is_discontinuous": True,
            "discontinuities": discontinuity_finder(x_range[0], x_range[1]) if discontinuity_finder else None
        }

        num_samples = calculate_enough_number_of_samples(self.plane.x_length)

        # 연속구간별 그래프 생성
        graph_segments = VGroup()
        for x_min, x_max in ranges:
            segment = self._plot_function_segment(
                func, x_min, x_max, num_samples,
                y_limit, color, stroke_width, **kwargs
            )
            # 세그먼트도 메타데이터 포함
            self._ensure_metadata(segment)
            segment.metadata = {
                "type": MobjectType.FUNCTION,
                "parent_name": name,
                "x_range": [x_min, x_max]
            }
            graph_segments.add(segment)

        # 불연속점 표시
        if show_discontinuities and discontinuities:
            discontinuity_lines = create_asymptote_lines(
                self.plane,
                discontinuities,
                **discontinuity_config
            )
            # 점근선 그룹에 메타데이터 설정
            self._ensure_metadata(discontinuity_lines)
            discontinuity_lines.metadata = {
                "type": "ASYMPTOTES",
                "parent_name": name
            }
            result_group.add(discontinuity_lines)

        result_group.add(graph_segments)
        self.add(result_group)
        return result_group

    def _plot_function_segment(self, func, x_min, x_max, num_samples, y_limit, color, stroke_width, **kwargs):
        """함수의 한 구간을 그리는 헬퍼 메서드"""
        # 구간의 길이에 비례하여 샘플 수 계산
        total_range = self.plane.x_range[1] - self.plane.x_range[0]
        interval_length = x_max - x_min
        interval_samples = int(num_samples * (interval_length / total_range))
        interval_samples = max(interval_samples, 50)  # 최소 샘플 수 보장

        # 샘플링
        x_values = np.linspace(x_min, x_max, interval_samples)
        y_values = [func(x) for x in x_values]

        # y값 범위 제한
        mask = np.abs(y_values) <= y_limit
        x_values = x_values[mask]
        y_values = np.array(y_values)[mask]

        # 구간 그래프 생성
        return self.plane.plot_line_graph(
            x_values=x_values,
            y_values=y_values,
            line_color=color,
            stroke_width=stroke_width,
            vertex_dot_style={"fill_opacity": 0},
            **kwargs
        )

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
                  position=None,  # (x,y) 좌표
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

        if position:
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
                      position=None,
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

    def add_brace(self,
                  mobject,
                  direction=DOWN,
                  name=None,
                  buff=0.1,
                  color=WHITE,
                  text=None,
                  text_color=None,
                  text_buff=0.1,
                  font_size=36):  # 텍스트 색상을 독립적으로 설정
        """Brace(중괄호) 추가 메서드

        Args:
            mobject: 브레이스를 추가할 객체
            direction: 브레이스의 방향 (DOWN, UP, LEFT, RIGHT)
            name: 브레이스의 이름 (None이면 자동생성)
            buff: 브레이스와 객체 사이의 간격
            color: 브레이스의 색상
            text: 브레이스에 표시할 텍스트 (선택사항)
            font_size: 텍스트의 크기
            text_color: 텍스트의 색상 (None이면 브레이스와 같은 색상)

        Returns:
            tuple: (Brace, MathTex or None) - 브레이스와 텍스트 객체 튜플
        """
        if name is None:
            name = f"brace_{len(list(self.iter_mobjects(obj_type='BRACE')))}"

        # Brace 객체 생성
        brace = Brace(
            mobject,
            direction=direction,
            buff=buff,
            color=color
        )

        # 메타데이터 설정
        self._ensure_metadata(brace)
        brace.metadata = {
            "type": "BRACE",
            "name": name,
            "direction": direction,
            "has_text": text is not None
        }

        self.add(brace)

        # 텍스트 생성 및 추가
        tex = None
        if (text):
            if (text_color is None):
                text_color = color

            tex = brace.get_tex(text, buff=text_buff)
            tex.set_font_size(font_size)
            tex.set_color(text_color)

            # 텍스트 메타데이터 설정
            self._ensure_metadata(tex)
            tex.metadata = {
                "type": "BRACE_TEXT",
                "name": f"{name}_text",
                "parent_brace": name
            }

            # 텍스트 객체 따로 추가
            self.add(tex)

        return (brace, tex)

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
