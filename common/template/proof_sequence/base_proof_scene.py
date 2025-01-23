from typing import List, override
from abc import ABC, abstractmethod
from manim import *
from .scrolling_group import ScrollingGroup
from .proof_scene_config import ProofSceneConfig


class BaseProofScene(Scene, ABC):
    config: ProofSceneConfig

    def __init__(self):
        super().__init__()
        base_config = ProofSceneConfig()
        self.config = self.configure(base_config)

    @abstractmethod
    def get_title(self) -> str:
        """증명 제목 반환"""
        pass

    @abstractmethod
    def get_intro_formula(self) -> str:
        """인트로에 보여줄 수식 반환"""
        pass

    @abstractmethod
    def get_proof_steps(self, step_group_index: int = 0) -> List[str]:
        """증명 단계별 수식 리스트 반환"""
        pass

    def before_steps(self) -> int:
        """증명 단계 실행 전 추가 액션을 위한 훅 메소드

        하위 클래스에서 이 메서드를 오버라이드하여 증명 단계 실행 전 추가 액션을 수행할 수 있습니다.
        """
        return 1

    def after_step(self, step_group_index: int) -> None:
        """증명 단계 실행 후 추가 액션을 위한 훅 메소드

        하위 클래스에서 이 메서드를 오버라이드하여 증명 단계 실행 후 추가 액션을 수행할 수 있습니다.
        """
        pass

    def after_qed(self) -> None:
        """QED 박스 표시 후 추가 액션을 위한 훅 메소드

        하위 클래스에서 이 메서드를 오버라이드하여 QED 박스 표시 후 추가 액션을 수행할 수 있습니다.
        """
        pass

    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        """설정 커스터마이징을 위한 템플릿 메소드

        하위 클래스에서 이 메서드를 오버라이드하여 설정을 커스터마이징할 수 있습니다.
        기본 구현은 설정을 그대로 반환합니다.

        Args:
            config: 기본 설정이 담긴 ProofSceneConfig 객체

        Returns:
            수정된 ProofSceneConfig 객체

        Examples:
            ```python
            class MyProof(BaseProofScene):
                def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
                    # 타이틀 색상 변경
                    config.title_colors = ["#FFD700", "#4B0082"]

                    # 수식 색상 변경
                    config.formula_color = BLUE

                    # 애니메이션 시간 조정
                    config.animation_pause = 0.3
                    config.title_display_time = 1.5

                    return config
            ```
        """
        return config

    def _show_intro_title(self) -> None:
        """타이틀 페이지 표시"""
        title = Text(
            self.get_title(),
            font_size=self.config.title_font_size,
            weight=BOLD
        ).shift(self.config.title_position)

        title.set_color_by_gradient(*self.config.title_colors)

        glowing_title = title.copy()
        glowing_title.set_stroke(**self.config.title_glow_primary)

        glowing_title2 = title.copy()
        glowing_title2.set_stroke(**self.config.title_glow_secondary)

        title_group = VGroup(glowing_title2, glowing_title, title)

        # 증명하고자 하는 공식
        formula = MathTex(
            self.get_intro_formula(),
            font_size=self.config.title_intro_formula_size,
            color=self.config.formula_color
        ).shift(self.config.title_vertical_offset)

        # 타이틀과 공식을 함께 표시하고 페이드아웃
        self.play(
            FadeIn(title_group),
            FadeIn(formula)
        )
        self.wait(self.config.title_display_time)
        self.play(
            FadeOut(title_group),
            FadeOut(formula)
        )

    def _create_formula_tex_group(self, rule: str) -> VGroup:
        """수식 문자열로부터 MathTex VGroup을 생성"""
        parts = rule.split('=')
        tex_group = VGroup()

        for i, part in enumerate(parts):
            tex_part = MathTex(
                ('=' if i > 0 else '') + part.strip(),
                font_size=self.config.font_size,
                color=self.config.formula_color
            )
            tex_group.add(tex_part)

        tex_group.arrange(RIGHT, buff=self.config.h_buff)
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
                    v_spacing_buff=self.config.v_spacing_buff
                )
            else:
                current_equal_pos = tex_group[1].get_left()[0]
                h_offset = equal_x_pos - current_equal_pos

                scroller.add_element(
                    self,
                    tex_group,
                    v_spacing=max_height,
                    v_spacing_buff=self.config.v_spacing_buff,
                    h_offset=h_offset
                )

            self.wait(self.config.animation_pause)

    def _emphasize_conclusion(
        self,
        formula_group: VGroup,
        color: ManimColor = None,
        qed_position: np.ndarray = DR
    ) -> None:
        """결론 수식을 강조하고 QED 박스 추가"""
        color = color or self.config.conclusion_color

        qed_box = MathTex(
            r"\blacksquare",
            font_size=self.config.qed_font_size,
            color=color
        ).next_to(
            formula_group,
            qed_position,
            buff=self.config.qed_buff
        ).shift(self.config.qed_shift)

        self.play(
            formula_group.animate.set_color(color),
            FadeIn(qed_box, scale=1.2),
            run_time=self.config.conclusion_animation_time
        )

    @override
    def construct(self):
        """Template method that defines the proof animation structure"""
        self.next_section("Initial Setup")

        self.next_section("Proof Intro")

        if not self.config.skip_intro_title:
            self._show_intro_title()

        self.next_section("Proof Steps")

        num_of_steps_group = self.before_steps()

        for i in range(num_of_steps_group):
            proof_steps = self.get_proof_steps(i)

            if proof_steps:
                formula_groups, max_height, equal_x_pos = self._prepare_formula_groups(
                    proof_steps
                )

                scroller = ScrollingGroup(
                    add_position=self.config.start_position,
                    opacity_gradient=True
                )

                self._add_formulas_to_scroller(
                    scroller,
                    formula_groups,
                    max_height,
                    equal_x_pos
                )

                # 마지막 수식이 존재하는 경우에만 결론 강조
                self._emphasize_conclusion(formula_groups[-1])

            if self.config.scene_end_pause > 0:
                self.wait(self.config.scene_end_pause)

            self.after_step(i)

        self.after_qed()
