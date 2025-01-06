from typing import override
from manim import *
from scrolling_group import ScrollingGroup, ScrollDirection


class DifferenciationRuleProof(Scene):
    # 클래스 레벨 상수
    FONT_SIZE = 60
    FORMULA_COLOR = GREEN
    V_SPACING_BUFF = 0.25
    H_BUFF = 0.2
    ANIMATION_PAUSE = 0.5

    @override
    def construct(self):
        # 시작 위치 상수
        START_POSITION = ORIGIN + DOWN

        # 모든 수식을 VGroup으로 미리 생성
        formula_groups = []
        max_height = 0
        equal_x_pos = None

        constant_multiple_rule = [
            r"\left\{c \cdot f(x)\right\}' = \lim_{h \to 0} \frac{c \cdot f(x+h) - c \cdot f(x)}{h}",
            r"= \lim_{h \to 0} \frac{c \cdot \left\{f(x+h) - f(x)\right\}}{h}",
            r"= c \cdot \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"= c \cdot f'(x)"
        ]

        for rule in constant_multiple_rule:
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
            formula_groups.append(tex_group)
            
            # 최대 높이 계산
            max_height = max(max_height, tex_group.height)
            
            # 첫 번째 수식에서 '=' 위치 저장
            if len(formula_groups) == 1:
                equal_x_pos = tex_group[1].get_left()[0]

        # ScrollingGroup 초기화 (고정 간격 사용)
        scroller = ScrollingGroup(
            add_position=START_POSITION,
            opacity_gradient=True
        )

        # 수식들을 순차적으로 추가
        for idx, tex_group in enumerate(formula_groups):
            if idx == 0:
                scroller.add_element(
                    self,
                    tex_group,
                    v_spacing=max_height,  # 고정 높이 사용
                    v_spacing_buff=self.V_SPACING_BUFF
                )
            else:
                # '=' 위치 맞추기
                current_equal_pos = tex_group[1].get_left()[0]
                h_offset = equal_x_pos - current_equal_pos

                scroller.add_element(
                    self,
                    tex_group,
                    v_spacing=max_height,  # 고정 높이 사용
                    v_spacing_buff=self.V_SPACING_BUFF,
                    h_offset=h_offset
                )

            self.wait(self.ANIMATION_PAUSE)

        self.wait()
