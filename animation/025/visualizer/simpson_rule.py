from manim import *


class SimpsonRuleVisualizer:
    def compute_simpson_data(self, integrand, domain, iteration_count):
        x_start, x_end = domain
        total_width = x_end - x_start
        data_list = []
        for step in range(iteration_count):
            subinterval_count = 2 ** step
            if subinterval_count < 2:
                # Skip because we need at least 2 subintervals for Simpson's rule
                continue
            subinterval_width = total_width / subinterval_count
            bounds = [x_start + i *
                      subinterval_width for i in range(subinterval_count + 1)]
            areas = []
            for i in range(0, subinterval_count, 2):
                x_left = bounds[i]
                x_mid = bounds[i+1]
                x_right = bounds[i+2]
                h0 = integrand(x_left)
                h1 = integrand(x_mid)
                h2 = integrand(x_right)
                area = subinterval_width * (h0 + 4*h1 + h2) / 3
                areas.append(area)
            data_list.append({
                'subinterval_count': subinterval_count,
                'subinterval_width': subinterval_width,
                'bounds': bounds,
                'areas': areas
            })
        return data_list

    def visualize(self, scene, integrand, domain, iteration_count=5, remove_after=True):
        x_start, x_end = domain

        approx_value = MathTex(
            r"\int_{-2}^{2} f(x) \, dx", font_size=36, color=YELLOW
        )
        approx_value.to_edge(RIGHT).shift(DOWN * 2.25 + LEFT)
        scene.play(Write(approx_value))

        iter_n_str = MathTex("n = 1", font_size=36, color=YELLOW_A)
        total_dx = x_end - x_start
        total_dx_str = f"{total_dx:.6f}".rstrip('0').rstrip('.')
        delta_x = MathTex(r"\Delta x", "=", total_dx_str, font_size=36)
        delta_x.set_color_by_tex_to_color_map({
            r"\Delta x": TEAL,
            "=": WHITE,
            total_dx_str: BLUE
        })

        iter_info_text = VGroup(iter_n_str, delta_x).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        ).to_corner(DL, buff=1)

        integral_value = MathTex("", font_size=48, color=YELLOW)
        scene.add(integral_value)

        prev_shapes = None
        prev_dots = None

        simpson_data = self.compute_simpson_data(
            integrand, domain, iteration_count)

        for step, data in enumerate(simpson_data):
            integral_value.become(MathTex("", font_size=48, color=YELLOW))

            subinterval_count = data['subinterval_count']
            subinterval_width = data['subinterval_width']
            bounds = data['bounds']
            areas = data['areas']

            shape_group = VGroup()
            dot_group = VGroup()
            accumulated_area = sum(areas)

            for i in range(0, subinterval_count, 2):
                x_left = bounds[i]
                x_mid = bounds[i+1]
                x_right = bounds[i+2]
                h0 = integrand(x_left)
                h1 = integrand(x_mid)
                h2 = integrand(x_right)

                points = [
                    scene.plane.c2p(x_left, 0),
                    scene.plane.c2p(x_left, h0),
                    scene.plane.c2p(x_mid, h1),
                    scene.plane.c2p(x_right, h2),
                    scene.plane.c2p(x_right, 0)
                ]

                shape = Polygon(*points, fill_opacity=0.3,
                                stroke_width=1, color=BLUE)
                shape_group.add(shape)

                dot1 = Dot(scene.plane.c2p(x_left, h0),
                           color=PINK, radius=0.05).set_z_index(10)
                dot2 = Dot(scene.plane.c2p(x_mid, h1), color=PINK,
                           radius=0.05).set_z_index(10)
                dot3 = Dot(scene.plane.c2p(x_right, h2),
                           color=PINK, radius=0.05).set_z_index(10)
                dot_group.add(dot1, dot2, dot3)

            formatted_area = f"{accumulated_area:.6f}".rstrip('0').rstrip('.')
            formatted_dx = f"{subinterval_width:.6f}".rstrip('0').rstrip('.')

            if prev_shapes:
                scene.play(
                    FadeOut(prev_shapes),
                    FadeOut(prev_dots),
                    Transform(iter_n_str,
                              MathTex(f"n = {subinterval_count}",
                                      font_size=36, color=YELLOW_A)
                              .move_to(iter_n_str)),
                    Transform(delta_x,
                              MathTex(r"\Delta x", "=",
                                      formatted_dx, font_size=36)
                              .set_color_by_tex_to_color_map({
                                  r"\Delta x": TEAL,
                                  "=": WHITE,
                                  formatted_dx: BLUE
                              })
                              .move_to(delta_x))
                )
            else:
                scene.play(FadeIn(iter_info_text))

            scene.play(Create(shape_group), Create(dot_group))

            integral_value.become(
                MathTex(f"\\approx {formatted_area}",
                        font_size=36, color=YELLOW)
            ).next_to(approx_value, DOWN, buff=0.25).shift(RIGHT * 0.5)

            prev_shapes = shape_group
            prev_dots = dot_group
            scene.wait()

        if remove_after:
            scene.play(
                FadeOut(prev_shapes),
                FadeOut(prev_dots),
                FadeOut(iter_info_text),
                FadeOut(integral_value)
            )
            scene.wait()
            return None, None

        return prev_shapes, iter_info_text
