from typing import List, override
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import BaseProofScene, ProofSceneConfig


class ConstantMultipleRuleProof(BaseProofScene):
    @override
    def construct(self):
        return super().construct()

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        config.scene_end_pause += 1
        return config

    @override
    def get_title(self) -> str:
        return "Proof of Constant Multiple Rule"

    @override
    @latex_factory()
    def get_intro_formula(self) -> str:
        return r"\left\{c \cdot f(x)\right\}' = c \cdot f'(x)"

    @override
    @latex_factory()
    def get_proof_steps(self) -> List[str]:
        steps = [
            r"\left\{c \cdot f(x)\right\}' = \lim_{h \to 0} \frac{c \cdot f(x+h) - c \cdot f(x)}{h}",
            r"= \lim_{h \to 0} \frac{c \cdot \left\{f(x+h) - f(x)\right\}}{h}",
            r"= \lim_{h \to 0} c \cdot \left\{\frac{f(x+h) - f(x)}{h}\right\}",
            r"= c \cdot \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"= c \cdot f'(x)"
        ]
        return steps
