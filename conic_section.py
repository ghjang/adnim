from manim import *
from common.enhanced_number_plane import EnhancedNumberPlane


def vertical_opening_parabola(x):
    return x**2


def directrix_line(x):
    return -0.25  # y = x²의 준선은 y = -0.25


class Parabola(Scene):
    def construct(self):
        plane = EnhancedNumberPlane(
            origin_config={
                "size": 0.025,
                "color": BLUE
            }
        ).scale(3)
        self.add(plane)

        # 포물선 그래프와 방정식 추가
        plane.plot_function(
            vertical_opening_parabola,
            x_range=[-4, 4],
            color=YELLOW,
            stroke_width=3
        )
        plane.add_tex_label(
            "y=x^2",
            (2, 2),
            color=YELLOW
        )

        # 초점 추가 (라벨 포함)
        plane.add_point(
            (0, 0.25),
            label="F",
            label_direction=UP + RIGHT/5,
            color=RED
        )

        # 준선 그래프와 방정식 라벨 추가
        plane.plot_function(
            directrix_line,
            x_range=[-20, 20],
            color=RED,
            stroke_width=2
        )

        # 준선의 방정식 라벨 추가
        plane.add_tex_label(
            "y=-\\frac{1}{4}",
            (3, -0.25),
            color=RED,
            direction=DOWN,
            buff=0.3
        )

        self.wait(1)

        self.play(plane.animate.scale(1.5))
        self.play(plane.animate.shift(DOWN))

        self.wait(2)
