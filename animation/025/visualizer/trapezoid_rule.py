from manim import *


class TrapezoidalRuleVisualizer:
    def compute_trapezoid_data(self, integrand, domain, iteration_count):
        """
        사다리꼴 공식 계산 결과를 반환
        Returns:
            A list of dict, where each dict has:
                'subinterval_count', 'subinterval_width', 'bounds', 'areas'
        """
        x_start, x_end = domain
        total_width = x_end - x_start
        data_list = []

        for step in range(iteration_count):
            subinterval_count = 2 ** step
            subinterval_width = total_width / subinterval_count
            bounds = [
                x_start + i * subinterval_width for i in range(subinterval_count + 1)
            ]
            areas = []

            for i in range(subinterval_count):
                x_left = bounds[i]
                x_right = bounds[i + 1]
                h1 = integrand(x_left)
                h2 = integrand(x_right)
                # 사다리꼴 면적 = (a+b)h/2
                area = (h1 + h2) * subinterval_width / 2
                areas.append(area)

            data_list.append({
                'subinterval_count': subinterval_count,
                'subinterval_width': subinterval_width,
                'bounds': bounds,
                'areas': areas
            })

        return data_list

    def _display_trapezoid_formula(self, scene):
        trapezoid_area_formula = MathTex(
            r"\text{Trapezoid Area} = \frac{1}{2} \cdot \Big[\text{Base}_1 + \text{Base}_2\Big] \cdot \text{Height}",
            font_size=26
        )
        formula = MathTex(
            r"\int_a^b f(x) \, dx \approx \sum_{i=1}^n \frac{1}{2} \cdot \Big[f(x_{i-1}) + f(x_i)\Big] \cdot \Delta x",
            font_size=26
        )
        delta_x_formula = MathTex(r"\Delta x = \frac{b - a}{n}", font_size=26)
        x_i_formula = MathTex(
            r"x_i = a + i \cdot \Delta x \quad \text{(for } i = 0, 1, 2, \dots, n \text{)}",
            font_size=26
        )

        formulas = VGroup(
            trapezoid_area_formula,
            formula,
            delta_x_formula,
            x_i_formula
        ).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        ).to_corner(UL, buff=0.5).shift(LEFT * 0.15).set_color(YELLOW)

        scene.play(Write(formulas))
        return formulas

    def _same_sign(self, a, b):
        return (a >= 0) == (b >= 0)

    def _calc_fill_bg(self, scene, x_left, x_right, h1, h2):
        if self._same_sign(h1, h2):
            color = BLUE if h1 >= 0 else PINK
            bg = Polygon(
                *[
                    scene.plane.c2p(x_left, 0),
                    scene.plane.c2p(x_left, h1),
                    scene.plane.c2p(x_right, h2),
                    scene.plane.c2p(x_right, 0)
                ],
                fill_color=color,
                fill_opacity=0.3,
                stroke_opacity=0
            )
            if h1 >= 0:
                return bg, None
            else:
                return None, bg
        else:
            if h1 >= 0:
                upper_pt1 = scene.plane.c2p(x_left, 0)
                upper_pt2 = scene.plane.c2p(x_left, h1)
                upper_pt3 = scene.plane.c2p(x_right, 0)

                lower_pt1 = scene.plane.c2p(x_left, 0)
                lower_pt2 = scene.plane.c2p(x_right, 0)
                lower_pt3 = scene.plane.c2p(x_right, h2)
            else:
                upper_pt1 = scene.plane.c2p(x_left, 0)
                upper_pt2 = scene.plane.c2p(x_right, 0)
                upper_pt3 = scene.plane.c2p(x_right, h2)

                lower_pt1 = scene.plane.c2p(x_left, h1)
                lower_pt2 = scene.plane.c2p(x_left, 0)
                lower_pt3 = scene.plane.c2p(x_right, 0)

            upper_part_fill_bg = Polygon(
                upper_pt1, upper_pt2, upper_pt3,
                fill_color=BLUE, fill_opacity=0.3, stroke_opacity=0
            )

            lower_part_fill_bg = Polygon(
                lower_pt1, lower_pt2, lower_pt3,
                fill_color=PINK, fill_opacity=0.3, stroke_opacity=0
            )

            return upper_part_fill_bg, lower_part_fill_bg

    def visualize(
        self,
        scene,
        integrand,
        domain,
        iteration_count=5,
        remove_after=True
    ):
        x_start, x_end = domain

        # 수식 표시
        formulas = self._display_trapezoid_formula(scene)

        approx_value = MathTex(
            r"\int_{-2}^{2} f(x) \, dx", font_size=36, color=YELLOW
        )
        approx_value.to_edge(RIGHT).shift(DOWN * 2.25 + LEFT)
        scene.play(Write(approx_value))

        # 왼쪽 하단 정보 표시
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

        prev_trapezoids = None
        prev_dots = None

        trapezoid_data = self.compute_trapezoid_data(
            integrand, domain, iteration_count)

        for step, data in enumerate(trapezoid_data):
            integral_value.become(MathTex("", font_size=48, color=YELLOW))

            subinterval_count = data['subinterval_count']
            subinterval_width = data['subinterval_width']
            bounds = data['bounds']
            areas = data['areas']

            trapezoid_group = VGroup()
            dot_group = VGroup()
            accumulated_area = sum(areas)

            for i in range(subinterval_count):
                x_left = bounds[i]
                x_right = bounds[i + 1]
                h1 = integrand(x_left)
                h2 = integrand(x_right)

                # 'delta x' 구간에서 함수의 양끝 값의 '부호'가 다를 경우에 정상적으로 그리기 위해서 리오더링 해줌.
                bl = scene.plane.c2p(x_left, min(0, h1))
                tl = scene.plane.c2p(x_left, max(0, h1))
                tr = scene.plane.c2p(x_right, max(0, h2))
                br = scene.plane.c2p(x_right, min(0, h2))
                points = [bl, tl, tr, br]

                trapezoid = Polygon(
                    *points,
                    fill_opacity=0
                ).set_z_index(5)
                trapezoid_group.add(trapezoid)

                upper_part_fill_bg, lower_part_fill_bg = self._calc_fill_bg(
                    scene,
                    x_left,
                    x_right,
                    h1,
                    h2
                )
                if upper_part_fill_bg:
                    trapezoid_group.add(upper_part_fill_bg)
                if lower_part_fill_bg:
                    trapezoid_group.add(lower_part_fill_bg)

                # 양 끝점 표시
                dot1 = Dot(scene.plane.c2p(x_left, h1),
                           color=PINK, radius=0.05).set_z_index(10)
                dot2 = Dot(scene.plane.c2p(x_right, h2),
                           color=PINK, radius=0.05).set_z_index(10)
                dot_group.add(dot1, dot2)

            formatted_area = f"{accumulated_area:.6f}".rstrip('0').rstrip('.')
            formatted_dx = f"{subinterval_width:.6f}".rstrip('0').rstrip('.')

            if prev_trapezoids:
                scene.play(
                    FadeOut(prev_trapezoids),
                    FadeOut(prev_dots),
                    Transform(iter_n_str,
                              MathTex(f"n = {2 ** step}",
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

            scene.play(Create(trapezoid_group), Create(dot_group))

            integral_value.become(
                MathTex(f"\\approx {formatted_area}",
                        font_size=36, color=YELLOW)
            ).next_to(approx_value, DOWN, buff=0.25).shift(RIGHT * 0.5)

            prev_trapezoids = trapezoid_group
            prev_dots = dot_group
            scene.wait()

        if remove_after:
            scene.play(
                FadeOut(prev_trapezoids),
                FadeOut(prev_dots),
                FadeOut(iter_info_text),
                FadeOut(integral_value),
                FadeOut(formulas)
            )
            scene.wait()
            return None, None

        return prev_trapezoids, iter_info_text
