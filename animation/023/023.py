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

    # 타이틀 관련 상수
    TITLE_FONT_SIZE = 64
    TITLE_POSITION = UP * 2
    TITLE_COLORS = ["#FFD700", "#50C878",
                    "#4B0082", "#800080"]  # 골드, 에메랄드, 인디고, 퍼플
    TITLE_GLOW_PRIMARY = {"color": "#FFD700", "width": 8, "opacity": 0.3}
    TITLE_GLOW_SECONDARY = {"color": "#50C878", "width": 4, "opacity": 0.2}

    # 결론 수식 관련 상수
    CONCLUSION_COLOR = PINK
    QED_FONT_SIZE = 36
    QED_BUFF = 0.2
    QED_SHIFT = UP * 0.25
    CONCLUSION_ANIMATION_TIME = 1

    def _create_formula_tex_group(self, rule: str) -> VGroup:
        """수식 문자열로부터 MathTex VGroup을 생성"""
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
        return tex_group

    def _prepare_formula_groups(
        self,
        formulas: list[str]
    ) -> tuple[list[VGroup], float, float]:
        """모든 수식 VGroup을 생성하고 최대 높이와 기준 등호 위치를 계산"""
        formula_groups = []
        max_height = 0
        equal_x_pos = None

        for rule in formulas:
            tex_group = self._create_formula_tex_group(rule)
            formula_groups.append(tex_group)

            max_height = max(max_height, tex_group.height)

            if len(formula_groups) == 1:
                equal_x_pos = tex_group[1].get_left()[0]

        return formula_groups, max_height, equal_x_pos

    def _add_formulas_to_scroller(
        self,
        scroller: ScrollingGroup,
        formula_groups: list[VGroup],
        max_height: float,
        equal_x_pos: float
    ) -> None:
        """수식들을 스크롤러에 순차적으로 추가"""
        for idx, tex_group in enumerate(formula_groups):
            if idx == 0:
                scroller.add_element(
                    self,
                    tex_group,
                    v_spacing=max_height,
                    v_spacing_buff=self.V_SPACING_BUFF
                )
            else:
                current_equal_pos = tex_group[1].get_left()[0]
                h_offset = equal_x_pos - current_equal_pos

                scroller.add_element(
                    self,
                    tex_group,
                    v_spacing=max_height,
                    v_spacing_buff=self.V_SPACING_BUFF,
                    h_offset=h_offset
                )

            self.wait(self.ANIMATION_PAUSE)

    def _show_intro_title(self) -> None:
        """타이틀 페이지 표시"""
        title = Text(
            "Proof of Constant Multiple Rule",
            font_size=self.TITLE_FONT_SIZE,
            weight=BOLD
        ).shift(self.TITLE_POSITION)

        title.set_color_by_gradient(*self.TITLE_COLORS)

        glowing_title = title.copy()
        glowing_title.set_stroke(**self.TITLE_GLOW_PRIMARY)

        glowing_title2 = title.copy()
        glowing_title2.set_stroke(**self.TITLE_GLOW_SECONDARY)

        title_group = VGroup(glowing_title2, glowing_title, title)

        # 증명하고자 하는 공식
        formula = MathTex(
            r"\left\{c \cdot f(x)\right\}' = c \cdot f'(x)",
            font_size=72,
            color=self.FORMULA_COLOR
        ).shift(DOWN * 0.5)

        # 타이틀과 공식을 함께 표시하고 페이드아웃
        self.play(
            FadeIn(title_group),
            FadeIn(formula)
        )
        self.wait(2)
        self.play(
            FadeOut(title_group),
            FadeOut(formula)
        )

    def _emphasize_conclusion(
        self,
        formula_group: VGroup,
        color: ManimColor = None,
        qed_position: np.ndarray = DR
    ) -> None:
        """결론 수식을 강조하고 QED 박스 추가"""
        color = color or self.CONCLUSION_COLOR

        # QED 박스 생성 및 배치
        qed_box = MathTex(
            r"\blacksquare",
            font_size=self.QED_FONT_SIZE,
            color=color
        ).next_to(
            formula_group,
            qed_position,
            buff=self.QED_BUFF
        ).shift(self.QED_SHIFT)

        # 수식 강조와 QED 박스 표시
        self.play(
            formula_group.animate.set_color(color),
            FadeIn(qed_box, scale=1.2),
            run_time=self.CONCLUSION_ANIMATION_TIME
        )

    @override
    def construct(self):
        self.next_section("Initial Setup")

        START_POSITION = ORIGIN + DOWN * 1.5

        self.next_section("Constant Multiple Rule Proof - Intro")
        self._show_intro_title()

        self.next_section("Constant Multiple Rule Proof")

        # 상수곱 미분 증명 수식 시퀀스
        constant_multiple_rule = [
            r"\left\{c \cdot f(x)\right\}' = \lim_{h \to 0} \frac{c \cdot f(x+h) - c \cdot f(x)}{h}",
            r"= \lim_{h \to 0} \frac{c \cdot \left\{f(x+h) - f(x)\right\}}{h}",
            r"= \lim_{h \to 0} c \cdot \left\{\frac{f(x+h) - f(x)}{h}\right\}",
            r"= c \cdot \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"= c \cdot f'(x)"
        ]

        # 수식 VGroup들과 관련 정보 준비
        formula_groups, \
            max_height, \
            equal_x_pos = self._prepare_formula_groups(
                constant_multiple_rule
            )

        # 스크롤러 초기화
        scroller = ScrollingGroup(
            add_position=START_POSITION,
            opacity_gradient=True
        )

        # 수식들을 스크롤러에 추가
        self._add_formulas_to_scroller(
            scroller,
            formula_groups,
            max_height,
            equal_x_pos
        )

        # 마지막 수식 강조 및 QED 추가
        self._emphasize_conclusion(formula_groups[-1])

        self.wait(2)
