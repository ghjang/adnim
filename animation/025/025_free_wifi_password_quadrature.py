from typing import override, List
from sympy import cos, sqrt, S, latex
from sympy.abc import x
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import BaseProofScene, ProofSceneConfig


class FreeWifiPasswordQuadrature(BaseProofScene):
    @override
    def get_title(self) -> str:
        return "Finding the FREE Wi-Fi Password"

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        config.skip_intro_title = True
        config.scene_end_pause = 0
        return config

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
        plane = NumberPlane(
            y_range=[-3.5, 4.5],
            background_line_style={
                "stroke_opacity": 0.4
            }
        ).add_coordinates()
        self.add(plane)

        integrand = (x**3 * cos(x/2) + S(1)/2) * sqrt(4 - x**2)
        integrand_latex = f"f(x) = {latex(integrand, **{'mul_symbol': 'dot'})}"

        def f(x): return float(integrand.subs('x', x))

        graph = plane.plot(f, x_range=[-2, 2], color=GREEN)

        f_latex = MathTex(
            integrand_latex,
            font_size=24,
            color=GREEN
        ).next_to(graph, RIGHT, buff=0.75).align_to(graph, UP)

        self.play(
            Create(graph),
            FadeIn(f_latex),
            run_time=2
        )
        self.wait()
