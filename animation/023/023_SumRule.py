from typing import override
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import (
    BaseProofScene,
    ProofSceneConfig,
    ProofStepItem,
)


class SumRuleProof(BaseProofScene):
    @override
    def construct(self):
        return super().construct()

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        config.start_position += LEFT * 0.5
        config.font_size = 42
        config.scene_end_pause += 1
        return config

    @override
    def get_title(self) -> str:
        return "Proof of Sum Rule"

    @override
    @latex_factory()
    def get_intro_formula(self) -> str:
        return r"\left\{f(x) + g(x)\right\}' = f'(x) + g'(x)"

    @override
    @latex_factory()
    def get_proof_steps(self, step_group_index: int) -> list[ProofStepItem]:
        steps = [
            r"\left\{f(x) + g(x)\right\}' = \lim_{h \to 0} \frac{\left\{f(x+h) + g(x+h)\right\} - \left\{f(x) + g(x)\right\}}{h}",
            r"= \lim_{h \to 0} \frac{f(x+h) + g(x+h) - f(x) - g(x)}{h}",
            r"= \lim_{h \to 0} \frac{f(x+h) - f(x) + g(x+h) - g(x)}{h}",
            r"= \lim_{h \to 0} \frac{\left\{f(x+h) - f(x)\right\} + \left\{g(x+h) - g(x)\right\}}{h}",
            r"= \lim_{h \to 0} \left\{ \frac{f(x+h) - f(x)}{h} + \frac{g(x+h) - g(x)}{h} \right\}",
            r"= \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} + \lim_{h \to 0} \frac{g(x+h) - g(x)}{h}",
            r"= f'(x) + g'(x)",
        ]

        return steps
