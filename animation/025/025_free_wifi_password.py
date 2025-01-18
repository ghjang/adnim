from typing import override, List
from sympy import cos, sqrt, symbols, S
from sympy.abc import x
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import BaseProofScene, ProofSceneConfig


class FreeWifiPasswordDefiniteIntegration(BaseProofScene):
    @override
    def construct(self):
        return super().construct()

    @override
    def get_title(self) -> str:
        return "Finding the FREE Wi-Fi Password"

    @override
    @latex_factory()
    def get_intro_formula(self) -> str:
        intro_formula = r"""
        \int_{-2}^{2} \left( x^3 \cdot \cos\frac{x}{2} + \frac{1}{2} \right) \cdot \sqrt{4 - x^2} \; dx
        """
        return intro_formula

    @override
    @latex_factory()
    def get_proof_steps(self) -> List[str]:
        steps = [
        ]
        return steps

    @override
    @latex_factory()
    def after_qed(self) -> None:
        integrand = (x**3 * cos(x/2) + S(1)/2) * sqrt(4 - x**2)
