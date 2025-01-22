from typing import override, List
from sympy import cos, sqrt, S, latex
from sympy.abc import x
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import BaseProofScene, ProofSceneConfig
from visualizer.trapezoid_rule import TrapezoidalRuleVisualizer


class FreeWifiPasswordTrapezoidalRule(BaseProofScene):
    @override
    def get_title(self) -> str:
        return "An Example of the Trapezoidal Rule"

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        self.integrand_f = (x**3 * cos(x/2) + S(1)/2) * sqrt(4 - x**2)
        self.integrand_f_latex = latex(
            self.integrand_f, **{'mul_symbol': 'dot'}
        )

        config.title_font_size = 54
        config.scene_end_pause = 0

        return config

    @override
    @latex_factory()
    def get_intro_formula(self) -> str:
        return rf"\int_{{-2}}^{{2}} {self.integrand_f_latex} \; dx"

    @override
    @latex_factory()
    def get_proof_steps(self) -> List[str]:
        steps = [
        ]
        return steps

    @override
    @latex_factory()
    def after_qed(self) -> None:
        self.next_section("Plotting the integrand")

        self.plane = NumberPlane(
            y_range=[-3.5, 4.5],
            background_line_style={
                "stroke_opacity": 0.4
            }
        ).add_coordinates()
        self.add(self.plane)

        def f(x): return float(self.integrand_f.subs('x', x))

        graph = self.plane.plot(f, x_range=[-2, 2], color=GREEN)
        f_latex = MathTex(
            f"f(x) = {self.integrand_f_latex}",
            font_size=26,
            color=GREEN
        ).next_to(graph, RIGHT, buff=0.5).align_to(graph, UP)

        self.play(Create(graph), FadeIn(f_latex), run_time=2)
        self.wait()

        self.next_section(
            "Calculating the Definite Integration Value by Trapezoidal Rule")

        trapezoidal = TrapezoidalRuleVisualizer()
        trapezoidal.visualize(
            self,
            f,
            (-2, 2),
            iteration_count=6,
            remove_after=False
        )

        self.wait(2)
