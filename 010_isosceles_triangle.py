from manim import *
from common.number_plane_group import *
import numpy as np


class IsoscelesTriangle(Scene):
    def construct(self):
        self.next_section("Initial Number Plane And Two Dots",
                          skip_animations=True)
        plane_group = NumberPlaneGroup(
            origin_style_type=OriginStyle.CROSS
        )
        self.add(plane_group)

        # x-y축의 직각 표시 추가
        right_angle = plane_group.add_right_angle_mark((0, 0))

        # 두 점 생성
        dot1 = plane_group.add_point(
            (5, 0),
            color=BLUE,
        )
        dot2 = plane_group.add_point(
            (-5, 0),
            color=BLUE,
        )
        self.play(FadeIn(dot1), FadeIn(dot2))

        self.next_section("Isosceles Triangle 1, Draw Arcs",
                          skip_animations=True)
        # dot1을 중심으로 B까지의 거리를 반지름으로 하는 호
        arc1 = plane_group.add_arc(
            center_point=(5, 0),
            radius=10,
            start_angle=PI/2,
            angle=PI,
            color=YELLOW_A,
            dash_length=0.1
        )
        self.play(Create(arc1))

        # dot2을 중심으로 B까지의 거리를 반지름으로 하는 호
        arc2 = plane_group.add_arc(
            center_point=(-5, 0),
            radius=10,
            start_angle=PI/2,
            angle=-PI,
            color=YELLOW_A,
            dash_length=0.1
        )
        self.play(Create(arc2))

        self.next_section(
            "Isosceles Triangle 1, Draw Intersection Points", skip_animations=True)

        # 두 원의 교점 계산
        # 두 점 사이의 거리 d = 10 (점 A와 B 사이)
        # 두 원의 반지름 r = 10
        # 교점의 y좌표 = ±√(r² - (d/2)²)
        # 교점의 x좌표 = 0 (중점)
        d = 10  # A와 B 사이의 거리
        r = 10  # 반지름
        y = np.sqrt(r**2 - (d/2)**2)  # 교점의 y좌표

        # 교점 표시
        intersection1 = plane_group.add_point(
            (0, y),     # 위쪽 교점
            color=RED,
        )
        intersection2 = plane_group.add_point(
            (0, -y),    # 아래쪽 교점
            color=RED,
        )

        self.play(
            FadeIn(intersection1),
            FadeIn(intersection2)
        )

        self.next_section("Isosceles Triangle 1, Draw Triangle",)

        # 이등변삼각형 그리기
        triangle = plane_group.add_triangle(
            p1=(5, 0),      # A점
            p2=(-5, 0),     # B점
            p3=(0, y),      # 상단 교점
            color=BLUE,
            fill_opacity=0.2  # 약간의 투명도로 채우기
        )

        self.play(Create(triangle))

        # 이등변삼각형의 같은 변에 마킹 추가
        left_marks = plane_group.add_equal_marks(
            (-5, 0), (0, y),
            num_marks=2,
            color=LIGHT_GRAY,
        )
        right_marks = plane_group.add_equal_marks(
            (5, 0), (0, y),
            num_marks=2,
            color=LIGHT_GRAY,
        )

        # 이등변삼각형의 밑각 표시 (수정)
        left_angle = plane_group.add_angle_mark(
            (0, y),      # 꼭대기 점
            (-5, 0),     # 밑점(꼭지점)
            (-4, 0),     # x축 양의 방향으로 약간 이동한 점
            color=LIGHT_BROWN,
            other_angle=True  # 실제 내각만 표시하도록 변경
        )
        right_angle = plane_group.add_angle_mark(
            (0, y),      # 꼭대기 점
            (5, 0),      # 밑점(꼭지점)
            (4, 0),      # x축 음의 방향으로 약간 이동한 점
            color=LIGHT_BROWN
        )

        # 두 밑각이 같음을 표시하는 호 추가
        # 삼각형의 각도 계산
        base_angle = np.arctan2(y, 5)  # 밑변과 이루는 각도

        # 왼쪽 밑각의 마커
        left_angle_mark = plane_group.add_equal_angle_marks(
            (-5, 0),    # 왼쪽 밑각의 꼭지점
            start_angle=base_angle,  # 왼쪽 밑변에서 시작
            angle=-base_angle,  # 음수 각도로 시계방향
            radius=0.5,  # 반지름 키움
            mark_size=0.2,
            color=LIGHT_BROWN,
            num_marks=2
        )

        # 오른쪽 밑각의 마커
        right_angle_mark = plane_group.add_equal_angle_marks(
            (5, 0),     # 오른쪽 밑각의 꼭지점
            start_angle=PI-base_angle,  # 오른쪽 밑변에서 시작
            angle=base_angle,  # 양수 각도로 반시계방향
            radius=0.5,  # 반지름 키움
            mark_size=0.2,
            color=LIGHT_BROWN,
            num_marks=2
        )

        self.play(
            FadeIn(left_marks),
            FadeIn(right_marks),
            FadeIn(left_angle),
            FadeIn(right_angle),
            FadeIn(left_angle_mark),
            FadeIn(right_angle_mark)
        )

        self.play(plane_group.animate.scale(1.1).shift(DOWN))

        self.wait(2)
