# fmt: off
import os
import sys

# Python path에 프로젝트 루트 추가
project_dir = os.path.abspath(os.getcwd())
sys.path.append(project_dir)

# 기본 라이브러리
from manim import *

# 사용자 정의 라이브러리
from common.number_plane_group import *
# fmt: on


class LineToCircle(Scene):
    def construct(self):
        npg = NumberPlaneGroup(
            axis_config={
                "stroke_opacity": 0.4
            },
            background_line_style={
                "stroke_opacity": 0.4
            }
        ).scale(4).shift(LEFT * 3.5)
        self.add(npg)

        unit_circle = npg.add_circle(center_point=[0, 0], radius=1, color=PINK)
        self.play(Create(unit_circle))

        unit_circle_tex = npg.add_tex_label(
            r"\text{Unit Circle, } r = 1",
            font_size=36,
            color=YELLOW
        )

        unit_circle_tex.next_to(unit_circle, DOWN)
        self.play(FadeIn(unit_circle_tex), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(unit_circle_tex))
        new_circle_pos = npg.plane.c2p(-1, 0)
        self.play(unit_circle.animate.move_to(new_circle_pos))
        self.wait()

        line_len = 2 * PI * 1
        line_end = npg.plane.c2p(line_len, 0)

        line = npg.add_line(ORIGIN, line_end, color=GREEN, stroke_width=6)
        brace, circumference_tex = npg.add_brace(
            line,
            direction=DOWN,
            color=GRAY,
            text=r"Circumference = 2 \times \pi \times 1 \approx {:.5f}"
            .format(line_len),
            text_color=YELLOW,
            text_buff=0.1,
            font_size=36
        )

        self.play(Create(line))
        self.play(
            FadeIn(brace),
            FadeIn(circumference_tex),
        )
        self.wait()

        self.play(
            line.copy().animate.become(unit_circle).set_color(GREEN),
            line.animate.set_opacity(0.3),
            brace.animate.set_opacity(0.3),
            run_time=4
        )

        self.wait(2)
