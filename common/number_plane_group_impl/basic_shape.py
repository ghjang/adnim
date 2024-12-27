from manim import *

from .number_plane_group_base import (
    MobjectType,
    NumberPlaneGroupBase
)

from ..angle_decoration import AngleMarker  # AngleMarker 클래스 임포트
from ..line_decoration import LineMarker  # LineMarker 클래스 임포트
from ..animation.rotate_vector import VECTOR_STYLE  # VECTOR_STYLE 임포트 추가

# FIXME
# 'add_xxx' 함수에 'stroke_width' 같은 파라미터가 있을 경우에
# 'plane'의 스케일 변환을 적용해 주어야함.
#
# 'add_point, add_line'은 적용한 상태임.      

class BasicShapeMixin(NumberPlaneGroupBase):
    def __init__(self, **kwargs):
        if not hasattr(self, '_init_called'):
            super().__init__(**kwargs)
        self._ensure_single_init()

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

        # radius를 화면 좌표계로 변환 (x축 기준으로 변환)
        radius_point = self.plane.c2p(radius, 0)
        origin_point = self.plane.c2p(0, 0)
        transformed_radius = np.linalg.norm(radius_point - origin_point)

        dot = Dot(
            point=self.plane.c2p(*point),
            radius=transformed_radius,
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

    def add_line(
        self,
        start_point,   # (x1, y1) 좌표
        end_point,     # (x2, y2) 좌표
        name=None,
        color=BLUE,
        stroke_width=2,
        dashed=False,       # 추가된 옵션
        dash_length=0.1,    # 원하는 대쉬 길이
        stroke_opacity=1.0  # 선 불투명도 추가 (기본값 1.0)
    ):
        """선 추가 메서드"""
        if name is None:
            name = f"line_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.LINE])}"

        # 시작점과 끝점의 좌표를 변환
        start = self.plane.c2p(*start_point)
        end = self.plane.c2p(*end_point)

        # stroke_width를 화면 좌표계로 변환 (x축 기준으로 변환)
        width_point = self.plane.c2p(stroke_width, 0)
        origin_point = self.plane.c2p(0, 0)
        transformed_stroke_width = np.linalg.norm(width_point - origin_point)

        # dash_length도 변환
        if dashed:
            dash_point = self.plane.c2p(dash_length, 0)
            transformed_dash_length = np.linalg.norm(dash_point - origin_point)

        # 선 객체 생성
        if dashed:
            line = DashedLine(
                start=start,
                end=end,
                color=color,
                stroke_width=transformed_stroke_width,
                dash_length=transformed_dash_length,
                stroke_opacity=stroke_opacity  # 불투명도 적용
            )
        else:
            line = Line(
                start=start,
                end=end,
                color=color,
                stroke_width=transformed_stroke_width,
                stroke_opacity=stroke_opacity  # 불투명도 적용
            )

        # 메타데이터 설정
        self._ensure_metadata(line)
        line.metadata = {
            "type": MobjectType.LINE,
            "name": name,
        }

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
