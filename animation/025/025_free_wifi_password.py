from typing import override, List
from sympy import cos, sqrt, symbols, S
from sympy.abc import x
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import BaseProofScene, ProofSceneConfig


class FreeWifiPasswordDefiniteIntegration(BaseProofScene):
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
    def get_proof_steps(self, step_group_index: int) -> List[str]:
        steps = [
        ]
        return steps

    @override
    @latex_factory()
    def after_qed(self) -> None:
        integrand = (x**3 * cos(x/2) + S(1)/2) * sqrt(4 - x**2)

        def f(x): return float(integrand.subs('x', x))

        plane = NumberPlane(
            y_range=[-3.5, 4.5],
            background_line_style={
                "stroke_opacity": 0.4
            }
        ).add_coordinates()

        graph = plane.plot(f, x_range=[-2, 2], color=GREEN)

        self.add(plane)
        self.play(
            Create(graph),
            run_time=2
        )
        self.wait()
