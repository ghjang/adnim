from typing import override
from manim import *
from _015_seven_deadly_sines_common import *


class SawtoothWave(CompositeHarmonicScene):
    """톱니파 플랏 애니메이션"""

    def __init__(self, **kwargs):
        super().__init__(
            n_components=7,
            color_theme='PASTEL',
            **kwargs
        )

    @override
    def construct(self):
        return super().construct()

    @override
    def create_title(self):
        title = Text("Plotting a Sawtooth Wave", font_size=68)
        title.set_color_by_gradient(PURPLE_E, GREEN_E, PINK, YELLOW_E)
        return title

    @override
    def create_formula_latex(self):
        elements = []
        elements.append(r"\sin(x)")
        for i in range(2, self.n_components + 1):
            elements.append("+")
            elements.append(r"\frac{\sin(" + str(i) + r"x)}{" + str(i) + r"}")

        color_map = {}
        term_index = 0
        for i, elem in enumerate(elements):
            if (elem != "+"):
                color_map[elem] = self.colors[f'VECTOR_{term_index + 1}']
                term_index += 1

        formula_latex = MathTex(*elements, tex_to_color_map=color_map)
        return formula_latex

    @override
    def create_graph_plot_function(self):
        n = self.n_components

        def sawtooth_wave_func(x):
            return sum(np.sin(k * x) / k for k in range(1, n + 1))

        return sawtooth_wave_func

    @override
    def create_circle_rotation_info(self, component_index):
        circle_radius = 1 / (component_index + 1)
        angular_velocity = component_index + 1
        return circle_radius, angular_velocity


class SquareWave(CompositeHarmonicScene):
    """사각파 플랏 애니메이션"""

    def __init__(self, **kwargs):
        super().__init__(
            n_components=7,
            color_theme='PASTEL',
            **kwargs
        )

    @override
    def construct(self):
        return super().construct()

    @override
    def create_title(self):
        title = Text("Plotting a Square Wave", font_size=68)
        title.set_color_by_gradient(PURPLE_E, GREEN_E, PINK, YELLOW_E)
        return title

    @override
    def create_formula_latex(self):
        elements = []
        elements.append(r"\sin(x)")
        for i in range(3, 2 * self.n_components, 2):
            elements.append("+")
            elements.append(f"\\frac{{\\sin({i}x)}}{{{i}}}")

        color_map = {}
        term_index = 0
        for i, elem in enumerate(elements):
            if (elem != "+"):
                color_map[elem] = self.colors[f'VECTOR_{term_index + 1}']
                term_index += 1

        formula_latex = MathTex(*elements, tex_to_color_map=color_map)
        return formula_latex

    @override
    def create_graph_plot_function(self):
        n = self.n_components

        def square_wave_func(x):
            return sum(np.sin(k * x) / k for k in range(1, 2 * n, 2))

        return square_wave_func

    @override
    def create_circle_rotation_info(self, component_index):
        circle_radius = 1 / (2 * (component_index + 1) - 1)
        angular_velocity = 2 * (component_index + 1) - 1
        return circle_radius, angular_velocity
