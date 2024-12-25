# fmt: off
import os
import sys

# Python path에 프로젝트 루트 추가
project_dir = os.path.abspath(os.getcwd())
sys.path.append(project_dir)

# 기본 라이브러리
from manim import *
import numpy as np

# 사용자 정의 라이브러리
from common.number_plane_group import *
# fmt: on


class IsoscelesTriangle(Scene):
    def construct(self):
        self.next_section("Initial Number Plane And Two Dots",
                          skip_animations=False)
        plane_group = NumberPlaneGroup(
            origin_config={
                "style": OriginStyle.CROSS
            }
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
                          skip_animations=False)
        # 두 원 추가 (채움 없이, 연한 선으로)
        circle1 = plane_group.add_circle(
            center_point=(5, 0),
            radius=10,
            color=PURPLE_A,
            fill_opacity=0,
            stroke_width=1.0,
            stroke_opacity=0.4
        )
        circle2 = plane_group.add_circle(
            center_point=(-5, 0),
            radius=10,
            color=PURPLE_A,
            fill_opacity=0,
            stroke_width=1.0,
            stroke_opacity=0.4
        )
        self.play(FadeIn(circle1), FadeIn(circle2))

        # dot1을 중심으로 B까지의 거리를 반지름으로 하는 호
        arc1 = plane_group.add_arc(
            center_point=(5, 0),
            radius=10,
            start_angle=PI/2,
            angle=PI,
            color=YELLOW,  # 더 선명한 노란색으로
            stroke_width=2,  # 호는 더 굵게
            dash_length=0.2  # 점선 간격 조정
        )
        self.play(Create(arc1))

        # dot2을 중심으로 B까지의 거리를 반지름으로 하는 호
        arc2 = plane_group.add_arc(
            center_point=(-5, 0),
            radius=10,
            start_angle=PI/2,
            angle=-PI,
            color=YELLOW,
            stroke_width=2,
            dash_length=0.2
        )
        self.play(Create(arc2))

        self.next_section(
            "Isosceles Triangle 1, Draw Intersection Points", skip_animations=False)

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
        self.play(plane_group.animate.scale(1.1).shift(DOWN))

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

        self.next_section("Isosceles Triangle 1, Add Angles And Markers")

        # 이등변삼각형의 같은 변에 마킹 추가
        left_marks = plane_group.add_line_marker(
            (-5, 0), (0, y),
            num_marks=2,
            color=LIGHT_GRAY,
            stroke_width=3
        )
        right_marks = plane_group.add_line_marker(
            (5, 0), (0, y),
            num_marks=2,
            color=LIGHT_GRAY,
            stroke_width=3
        )

        # 이등변삼각형의 밑각 표시
        angle_radius = 0.4  # 각의 반지름 지정

        # 왼쪽 밑각과 마커 (수정)
        left_angle = plane_group.add_angle(
            (-4, 0),     # x축 음의 방향으로 이동한 점 (순서 변경)
            (-5, 0),     # 밑점(꼭지점)
            (0, y),      # 꼭대기 점 (순서 변경)
            radius=angle_radius,
            color=LIGHT_BROWN
        )
        left_angle_mark = plane_group.add_angle_marker(
            left_angle,
            mark_size=0.15,
            color=LIGHT_BROWN,
            stroke_width=3
        )

        # 오른쪽 밑각과 마커
        right_angle = plane_group.add_angle(
            (0, y),
            (5, 0),
            (4, 0),
            radius=angle_radius,
            color=LIGHT_BROWN
        )
        right_angle_mark = plane_group.add_angle_marker(
            right_angle,  # Angle 객체 직접 전달
            mark_size=0.15,
            color=LIGHT_BROWN,
            stroke_width=3
        )

        self.play(
            FadeIn(left_marks),
            FadeIn(right_marks),
            FadeIn(left_angle),
            FadeIn(right_angle),
            FadeIn(left_angle_mark),
            FadeIn(right_angle_mark)
        )

        self.wait(2)
