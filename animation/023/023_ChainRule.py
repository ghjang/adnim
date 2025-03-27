from typing import override
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import (
    BaseProofScene,
    ProofSceneConfig,
    ProofStepItem,
)


class ChainRuleProof(BaseProofScene):
    @override
    def construct(self):
        return super().construct()

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        config.start_position += LEFT * 2.5
        config.font_size = 42
        config.scene_end_pause += 1
        return config

    @override
    def get_title(self) -> str:
        return "Proof of Chain Rule"

    @override
    @latex_factory()
    def get_intro_formula(self) -> str:
        return r"\frac{d}{dx}f(g(x)) = f'(g(x)) \cdot g'(x)"

    @override
    @latex_factory()
    def get_proof_steps(self, step_group_index: int) -> list[ProofStepItem]:
        steps = [
            r"\frac{d}{dx}f(g(x)) = \lim_{h \to 0} \frac{f(g(x+h)) - f(g(x))}{h}",
            r"= 1 \cdot \left\{ \lim_{h \to 0} \frac{f(g(x+h)) - f(g(x))}{h} \right\}",
            {
                "text": r"1 = \frac{g(x+h) - g(x)}{g(x+h) - g(x)}",
                "color": RED,
                "h_offset": RIGHT * 0.75,
            },
            r"= \left\{ \frac{g(x+h) - g(x)}{g(x+h) - g(x)} \right\} \cdot \left\{ \lim_{h \to 0} \frac{f(g(x+h)) - f(g(x))}{h} \right\}",
            r"= \lim_{h \to 0} \left\{ \frac{g(x+h) - g(x)}{g(x+h) - g(x)} \right\} \cdot \left\{ \frac{f(g(x+h)) - f(g(x))}{h} \right\}",
            r"= \lim_{h \to 0} \left\{ \frac{f(g(x+h)) - f(g(x))}{h} \right\} \cdot \left\{ \frac{g(x+h) - g(x)}{g(x+h) - g(x)} \right\}",
            r"= \lim_{h \to 0} \frac{\left\{f(g(x+h)) - f(g(x))\right\} \cdot \left\{g(x+h) - g(x)\right\}}{h \cdot \left\{g(x+h) - g(x)\right\}}",
            r"= \lim_{h \to 0} \frac{\left\{f(g(x+h)) - f(g(x))\right\} \cdot \left\{g(x+h) - g(x)\right\}}{\left\{g(x+h) - g(x)\right\} \cdot h}",
            r"= \lim_{h \to 0} \left\{\frac{f(g(x+h)) - f(g(x))}{g(x+h) - g(x)}\right\} \cdot \left\{\frac{g(x+h) - g(x)}{h}\right\}",
            r"= \lim_{h \to 0} \left\{\frac{f(g(x+h)) - f(g(x))}{g(x+h) - g(x)}\right\} \cdot \lim_{h \to 0} \left\{\frac{g(x+h) - g(x)}{h}\right\}",
            {
                "text": r"h = \Delta x, \quad g(x+h) - g(x) = \Delta g, \quad f(g(x+h)) - f(g(x)) = \Delta f",
                "color": RED,
                "h_offset": RIGHT * 3,
            },
            r"= \lim_{\Delta g \to 0} \frac{\Delta f}{\Delta g} \cdot \lim_{\Delta x \to 0} \frac{\Delta g}{\Delta x}",
            r"= \frac{df}{dg} \cdot \frac{dg}{dx}",
            r"= f'(g(x)) \cdot g'(x)",
        ]

        return steps
