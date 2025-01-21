from manim import *
from enum import Enum


class RiemannSumType(Enum):
    LOWER = 'lower'
    UPPER = 'upper'
    MIDPOINT = 'midpoint'


class RiemannSumVisualizer:
    def __init__(self, sum_type=RiemannSumType.MIDPOINT):
        self.sum_type = sum_type

    def compute_riemann_data(self, integrand, domain, iteration_count):
        """
        리만 합 계산 결과를 반환.
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
                if self.sum_type == RiemannSumType.LOWER:
                    x_sample = bounds[i]
                elif self.sum_type == RiemannSumType.UPPER:
                    x_sample = bounds[i + 1]
                else:
                    x_sample = (bounds[i] + bounds[i + 1]) / 2
                height = integrand(x_sample)
                areas.append(height * subinterval_width)

            data_list.append({
                'subinterval_count': subinterval_count,
                'subinterval_width': subinterval_width,
                'bounds': bounds,
                'areas': areas
            })

        return data_list

    def _display_lower_riemann_formula(self, scene):
        formula_lower = MathTex(
            r"\int_a^b f(x) \, dx \approx \sum_{i=0}^{n-1} f(x_{i}) \cdot \Delta x",
            font_size=26
        )
        delta_x_formula = MathTex(r"\Delta x = \frac{b - a}{n}", font_size=26)
        x_i_formula = MathTex(
            r"x_i = a + i \cdot \Delta x \quad \text{(for } i = 0, 1, 2, \dots, n \text{)}",
            font_size=26
        )
        formulas = VGroup(
            formula_lower,
            delta_x_formula,
            x_i_formula
        ).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        ).to_corner(UL, buff=0.5).shift(LEFT * 0.15).set_color(YELLOW)

        scene.play(Write(formulas))
        return formulas

    def _display_midpoint_riemann_formula(self, scene):
        approx_formula = MathTex(
            r"\int_a^b f(x) \, dx \approx \sum_{i=1}^n f(x_i^{\text{mid}}) \cdot \Delta x",
            font_size=26
        )

        x_i_formula = MathTex(
            r"x_i = a + i \cdot \Delta x \quad \text{(for } i = 0, 1, 2, \dots, n \text{)}",
            font_size=26
        )

        x_i_mid_formula = MathTex(
            r"x_i^{\text{mid}} = \frac{x_{i-1} + x_i}{2} = a + \left(i - \frac{1}{2}\right) \cdot \Delta x",
            font_size=26
        )

        delta_x_formula = MathTex(r"\Delta x = \frac{b - a}{n}", font_size=26)

        formulas = VGroup(
            approx_formula,
            delta_x_formula,
            x_i_formula,
            x_i_mid_formula
        ).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        ).to_corner(UL, buff=0.5).shift(LEFT * 0.15).set_color(YELLOW)

        scene.play(Write(formulas))

        return formulas

    def _display_upper_riemann_formula(self, scene):
        formula_upper = MathTex(
            r"\int_a^b f(x) \, dx \approx \sum_{i=1}^n f(x_i) \cdot \Delta x",
            font_size=26
        )
        delta_x_formula = MathTex(r"\Delta x = \frac{b - a}{n}", font_size=26)
        x_i_formula = MathTex(
            r"x_i = a + i \cdot \Delta x \quad \text{(for } i = 0, 1, 2, \dots, n \text{)}",
            font_size=26
        )
        formulas = VGroup(
            formula_upper,
            delta_x_formula,
            x_i_formula
        ).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        ).to_corner(UL, buff=0.5).shift(LEFT * 0.15).set_color(YELLOW)

        scene.play(Write(formulas))
        return formulas

    def visualize(
        self,
        scene,
        integrand,
        domain,
        iteration_count=5,
        remove_after=True
    ):
        """Midpoint Riemann Sum 시각화

        Args:
            integrand: 적분 대상 함수
            domain: 적분 구간 (시작값, 끝값)
            iteration_count: 반복 횟수 (2^n 분할)
            remove_after: 마지막 이터레이션 후 결과를 지울지 여부

        Returns:
            rectangles: 마지막 사각형들
            value_text: 마지막 텍스트 그룹
        """
        x_start, x_end = domain

        if self.sum_type == RiemannSumType.LOWER:
            formulas = self._display_lower_riemann_formula(scene)
        if self.sum_type == RiemannSumType.MIDPOINT:
            formulas = self._display_midpoint_riemann_formula(scene)
        if self.sum_type == RiemannSumType.UPPER:
            formulas = self._display_upper_riemann_formula(scene)

        approx_value = MathTex(
            r"\int_{-2}^{2} f(x) \, dx", font_size=36, color=YELLOW
        )
        approx_value.to_edge(RIGHT).shift(DOWN * 2.25 + LEFT)
        scene.play(Write(approx_value))

        # 왼쪽 하단 정보 표시: n값과 델타x
        iter_n_str = MathTex("n = 1", font_size=36, color=YELLOW_A)

        # 델타 x 표시
        total_dx = x_end - x_start
        total_dx_str = f"{total_dx:.6f}".rstrip('0').rstrip('.')
        delta_x = MathTex(r"\Delta x", "=", total_dx_str, font_size=36)
        delta_x.set_color_by_tex_to_color_map({
            r"\Delta x": TEAL,
            "=": WHITE,
            total_dx_str: BLUE
        })

        # 왼쪽 하단에 정보 배치
        iter_info_text = VGroup(iter_n_str, delta_x).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        ).to_corner(DL, buff=1)

        # 적분값 표시 (오른쪽 화면 중앙)
        integral_value = MathTex("", font_size=48, color=YELLOW)
        scene.add(integral_value)

        prev_rectangles = None
        prev_dots = None

        riemann_data = self.compute_riemann_data(
            integrand, domain, iteration_count)

        for step, data in enumerate(riemann_data):
            integral_value.become(MathTex("", font_size=48, color=YELLOW))

            subinterval_count = data['subinterval_count']
            subinterval_width = data['subinterval_width']
            bounds = data['bounds']
            areas = data['areas']

            subinterval_rects = VGroup()
            dot_group = VGroup()
            accumulated_area = sum(areas)

            for i in range(subinterval_count):
                x_left = bounds[i]
                x_right = bounds[i + 1]
                # 샘플링 좌표 결정
                if self.sum_type == RiemannSumType.LOWER:
                    x_sample = x_left
                    anchor_edge = LEFT
                elif self.sum_type == RiemannSumType.UPPER:
                    x_sample = x_right
                    anchor_edge = RIGHT
                else:  # MIDPOINT
                    x_sample = (x_left + x_right) / 2
                    anchor_edge = None

                height = areas[i] / subinterval_width

                rect = Rectangle(
                    width=subinterval_width,
                    height=abs(height),
                    fill_opacity=0.3,
                    stroke_width=1,
                    color=BLUE if height >= 0 else "#FF69B4"
                )
                # 수평 위치 맞추기
                if anchor_edge is not None:
                    rect.move_to(scene.plane.c2p(x_sample, 0),
                                 aligned_edge=anchor_edge)
                else:
                    rect.move_to(scene.plane.c2p(x_sample, 0))

                # 수직 위치 맞추기
                if height >= 0:
                    rect.align_to(scene.plane.c2p(0, 0), DOWN)
                else:
                    rect.align_to(scene.plane.c2p(0, 0), UP)

                dot = Dot(
                    point=scene.plane.c2p(x_sample, height),
                    color=PINK,
                    radius=0.05
                ).set_z_index(10)
                dot_group.add(dot)
                subinterval_rects.add(rect)

            formatted_area = f"{accumulated_area:.6f}".rstrip('0').rstrip('.')
            formatted_dx = f"{subinterval_width:.6f}".rstrip('0').rstrip('.')

            # n값 업데이트 (이터레이션 텍스트만)
            if prev_rectangles:
                scene.play(
                    FadeOut(prev_rectangles),
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

            # 사각형과 점들 생성
            scene.play(Create(subinterval_rects), Create(dot_group))

            # 적분값 업데이트
            integral_value.become(
                MathTex(f"\\approx {formatted_area}",
                        font_size=36, color=YELLOW)
            ).next_to(approx_value, DOWN, buff=0.25).shift(RIGHT * 0.5)

            prev_rectangles = subinterval_rects
            prev_dots = dot_group
            scene.wait(2)

        # 마지막 상태 처리
        if remove_after:
            scene.play(
                FadeOut(prev_rectangles),
                FadeOut(prev_dots),
                FadeOut(iter_info_text),
                FadeOut(integral_value),
                FadeOut(formulas)
            )
            scene.wait()
            return None, None

        return prev_rectangles, iter_info_text
