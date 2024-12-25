import numpy as np
from manim import *
from common.number_plane_group import *
from common.trig_func import *


class TanGraphWithAsymptotes(Scene):
    def construct(self):
        # 축 생성
        axes = Axes(
            x_range=[-PI, PI, PI/4],
            y_range=[-12, 12, 1],
            x_length=6,
            axis_config={"color": BLUE},
            tips=False
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        x_ranges, discontinuities = calculate_tan_ranges(
            axes.x_range[0],
            axes.x_range[1]
        )

        asymptote_lines = create_asymptote_lines(axes, discontinuities)

        num_samples = calculate_enough_number_of_samples(axes.x_length)
        tan_segments = create_tan_segments(
            axes,
            x_ranges,
            num_samples
        )

        self.play(Create(axes), Write(labels))
        self.play(Create(asymptote_lines))
        self.play(Create(tan_segments))
        self.wait(2)


class TanGraphWithAsymptotesOnPlane(Scene):
    def construct(self):
        # NumberPlane 생성 (좌표축 포함)
        plane = NumberPlane(
            x_range=[-PI, PI, PI/4],
            y_range=[-12, 12, 1],
            x_length=6,
            y_length=6,
            axis_config={
                "color": BLUE,
                # "include_numbers": True,  # 축에 숫자 표시
                "decimal_number_config": {"num_decimal_places": 1}  # 소수점 자리수
            },
            background_line_style={
                "stroke_opacity": 0.3,
            }
        )
        # plane.add_coordinates()  # 좌표 눈금 추가

        # 축 라벨 추가
        x_label = MathTex("x").next_to(plane.x_axis, RIGHT)
        y_label = MathTex("y").next_to(plane.y_axis, UP)
        labels = VGroup(x_label, y_label)

        # 연속구간과 불연속점 계산
        x_ranges, discontinuities = calculate_tan_ranges(
            plane.x_range[0],
            plane.x_range[1]
        )

        # 점근선 생성
        asymptote_lines = create_asymptote_lines(plane, discontinuities)

        # 탄젠트 그래프 세그먼트 생성
        num_samples = calculate_enough_number_of_samples(plane.x_length)
        tan_segments = create_tan_segments(
            plane,
            x_ranges,
            num_samples
        )

        # 애니메이션 실행
        self.play(Create(plane))
        self.play(Write(labels))
        self.play(Create(asymptote_lines))
        self.play(Create(tan_segments))
        self.wait(2)
