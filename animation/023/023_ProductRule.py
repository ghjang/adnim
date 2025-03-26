from typing import override
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import (
    BaseProofScene,
    ProofSceneConfig,
    ProofStepItem,
)


class ProductRuleProof(BaseProofScene):
    @override
    def construct(self):
        return super().construct()

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        config.title_intro_formula_size = 62
        config.font_size = 38
        config.equal_symbol_h_extra_offset = LEFT * 4.75
        config.scene_end_pause += 1
        return config

    @override
    def get_title(self) -> str:
        return "Proof of Product Rule"

    @override
    @latex_factory()
    def get_intro_formula(self) -> str:
        return r"\left\{f(x) \cdot g(x)\right\}' = f(x) \cdot g'(x) + f'(x) \cdot g(x)"

    @override
    @latex_factory()
    def get_proof_steps(self, step_group_index: int) -> list[ProofStepItem]:
        steps = [
            r"\left\{f(x) \cdot g(x)\right\}' = \lim_{h \to 0} \frac{f(x+h) \cdot g(x+h) - f(x) \cdot g(x)}{h}",
            {
                "text": r"f(x+h) \cdot g(x) - f(x+h) \cdot g(x) = 0",
                "color": RED,
                "h_offset": RIGHT * 3.55,
            },
            r"= \lim_{h \to 0} \frac{f(x+h) \cdot g(x+h) - f(x) \cdot g(x) + \left\{f(x+h) \cdot g(x) - f(x+h) \cdot g(x)\right\}}{h}",
            r"= \lim_{h \to 0} \frac{f(x+h) \cdot g(x+h) - f(x) \cdot g(x) + f(x+h) \cdot g(x) - f(x+h) \cdot g(x)}{h}",
            r"= \lim_{h \to 0} \frac{f(x+h) \cdot g(x+h) - f(x+h) \cdot g(x) - f(x) \cdot g(x) + f(x+h) \cdot g(x)}{h}",
            r"= \lim_{h \to 0} \frac{\left\{f(x+h) \cdot g(x+h) - f(x+h) \cdot g(x)\right\} + \left\{-f(x) \cdot g(x) + f(x+h) \cdot g(x)\right\}}{h}",
            r"= \lim_{h \to 0} \frac{\left\{f(x+h) \cdot g(x+h) - f(x+h) \cdot g(x)\right\} + \left\{f(x+h) \cdot g(x) - f(x) \cdot g(x)\right\}}{h}",
            r"= \lim_{h \to 0} \left\{\frac{f(x+h) \cdot g(x+h) - f(x+h) \cdot g(x)}{h} + \frac{f(x+h) \cdot g(x) - f(x) \cdot g(x)}{h}\right\}",
            r"= \lim_{h \to 0} \left[\frac{f(x+h) \cdot \left\{g(x+h) - g(x)\right\}}{h} + \frac{g(x) \cdot \left\{f(x+h) - f(x)\right\}}{h} \right]",
            r"= \lim_{h \to 0} \left\{f(x+h) \cdot \frac{g(x+h) - g(x)}{h} + g(x) \cdot \frac{f(x+h) - f(x)}{h} \right\}",
            r"= \lim_{h \to 0} \left\{f(x+h) \cdot \frac{g(x+h) - g(x)}{h}\right\} + \lim_{h \to 0} \left\{g(x) \cdot \frac{f(x+h) - f(x)}{h}\right\}",
            r"= \lim_{h \to 0} f(x+h) \cdot \lim_{h \to 0} \frac{g(x+h) - g(x)}{h} + \lim_{h \to 0} g(x) \cdot \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"= f(x) \cdot \lim_{h \to 0} \frac{g(x+h) - g(x)}{h} + g(x) \cdot \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"= f(x) \cdot g'(x) + g(x) \cdot f'(x)",
            r"= f(x) \cdot g'(x) + f'(x) \cdot g(x)",
        ]

        return steps
