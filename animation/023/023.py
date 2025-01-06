from typing import override
from manim import *
from scrolling_group import ScrollingGroup, ScrollDirection


class DifferenciationRuleProof(Scene):
    # 클래스 레벨 상수
    FONT_SIZE = 48
    FORMULA_COLOR = GREEN
    V_SPACING_BUFF = 0.2
    H_BUFF = 0.2
    ANIMATION_PAUSE = 0.5

    @override
    def construct(self):
        # 시작 위치 상수
        START_POSITION = ORIGIN + DOWN

        scroller = ScrollingGroup(
            add_position=START_POSITION,
            opacity_gradient=True
        )

        constant_multiple_rule = [
            r"\left\{c \cdot f(x)\right\}' = \lim_{h \to 0} \frac{c \cdot f(x+h) - c \cdot f(x)}{h}",
            r"= c \cdot \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"= c \cdot f'(x)"
        ]

        equal_x_pos = None  # '=' 문자의 x 좌표를 저장할 변수

        for idx, rule in enumerate(constant_multiple_rule):
            parts = rule.split('=')
            tex_group = VGroup()

            for i, part in enumerate(parts):
                tex_part = MathTex(
                    ('=' if i > 0 else '') + part.strip(),
                    font_size=self.FONT_SIZE,
                    color=self.FORMULA_COLOR
                )
                tex_group.add(tex_part)

            tex_group.arrange(RIGHT, buff=self.H_BUFF)

            if idx == 0:
                # 첫 번째 수식에서 '=' 문자의 위치를 저장
                scroller.add_element(
                    self,
                    tex_group,
                    v_spacing_buff=self.V_SPACING_BUFF,
                )
                # '=' 문자는 두 번째 텍스트 객체의 왼쪽 끝에 있음
                equal_x_pos = tex_group[1].get_left()[0]
            else:
                # 나머지 수식들은 '=' 위치를 맞추기 위해 h_offset 계산
                current_equal_pos = tex_group[1].get_left()[0]
                h_offset = equal_x_pos - current_equal_pos

                scroller.add_element(
                    self,
                    tex_group,
                    v_spacing_buff=self.V_SPACING_BUFF,
                    h_offset=h_offset
                )

            self.wait(self.ANIMATION_PAUSE)

        self.wait()
