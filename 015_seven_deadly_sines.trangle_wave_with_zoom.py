from typing import override
from manim import *
from _015_seven_deadly_sines_common import *


class TriangleWave(CompositeHarmonicScene):
    """삼각파 플랏 애니메이션"""

    def __init__(self, **kwargs):
        zoom_kwargs = {
            'zoom_factor': 0.4,
            'zoomed_display_width': 3.75,
            'zoomed_display_height': 3.75,
            'zoomed_camera_config': {'default_frame_stroke_width': 1},
            'zoomed_camera_frame_starting_position': [0, 0, 0]
        }

        super().__init__(
            n_components=7,
            main_scale=8,
            transformed_scale=1.2,
            left_edge_buff=0.25,
            right_edge_buff=0.25,
            final_rotation_run_time=8,
            color_theme='PASTEL',
            **zoom_kwargs,
            **kwargs
        )

    def _update_src_frame_position(self, sine_wave_manager):
        first_radius_vector_end = sine_wave_manager.vectors[0].get_end()
        self.src_frame.move_to(first_radius_vector_end)

    @override
    def construct(self):
        return super().construct()

    @override
    def create_title(self):
        title = Text("Plotting a Triangle Wave", font_size=68)
        title.set_color_by_gradient(PURPLE_E, GREEN_E, PINK, YELLOW_E)
        return title

    @override
    def before_initial_rotation(self, sine_wave_manager):
        self.src_frame = self.zoomed_camera.frame
        self._update_src_frame_position(sine_wave_manager)
        self.zoomed_display.to_edge(DL, buff=0.1)
        self.activate_zooming()

    @override
    def initial_rotation_update(self, sine_wave_manager, alpha):
        # if alpha == 0.5:
        #     self.zoomed_display.to_edge(UL, buff=0.1)

        self._update_src_frame_position(sine_wave_manager)

    @override
    def after_initial_rotation(self, sine_wave_manager):
        self.play(
            FadeOut(self.src_frame),
            FadeOut(self.zoomed_display),
            run_time=0.5
        )

    @override
    def create_formula_latex(self):
        elements = []
        elements.append(r"\sin(x)")
        for i in range(3, 2 * self.n_components, 2):
            elements.append("-" if (i-1)//2 % 2 == 1 else "+")
            elements.append(f"\\frac{{\\sin({i}x)}}{{{i}^2}}")

        color_map = {}
        term_index = 0
        for i, elem in enumerate(elements):
            if (elem not in ["+", "-"]):
                color_map[elem] = self.colors[f'VECTOR_{term_index + 1}']
                term_index += 1

        formula_latex = MathTex(*elements, tex_to_color_map=color_map)
        return formula_latex

    @override
    def create_plot_plane_config(self):
        default_config = super().create_plot_plane_config()
        return {
            'x_range': [-1, 4 * PI, 1],
            'y_range': default_config['y_range'],
            'x_length': 1 + 2 * PI,
            'y_length': default_config['y_length'],
        }

    @override
    def create_graph_plot_function(self):
        n = self.n_components

        def triangle_wave_func(x):
            return sum(
                ((-1)**((k-1)//2)) * np.sin(k * x) / (k*k)
                for k in range(1, 2 * n, 2)
            )

        return triangle_wave_func

    @override
    def create_circle_rotation_info(self, component_index):
        k = 2 * component_index + 1  # 1, 3, 5, 7, ...
        circle_radius = 1 / (k * k)  # 1, 1/9, 1/25, 1/49, ...

        # component_index는 '0-base'
        # '홀수'번째 항의 부호는 '+'
        # '짝수'번째 항의 부호는 '-'
        angular_velocity = k if component_index % 2 == 0 else -k

        return circle_radius, angular_velocity
