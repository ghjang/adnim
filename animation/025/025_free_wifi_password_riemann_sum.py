from typing import override, List
from sympy import cos, sqrt, S, latex
from sympy.abc import x
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import BaseProofScene, ProofSceneConfig


class FreeWifiPasswordMidPointRiemannSum(BaseProofScene):
    @override
    def get_title(self) -> str:
        return "An Example of a Midpoint Riemann Sum"

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        self.integrand_f = (x**3 * cos(x/2) + S(1)/2) * sqrt(4 - x**2)
        self.integrand_f_latex = latex(
            self.integrand_f, **{'mul_symbol': 'dot'})

        # config.skip_intro_title = True
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

    def _visualize_riemann_sum(
        self,
        integrand,
        domain: tuple[float, float],
        iteration_count: int = 5,
        remove_after: bool = True
    ) -> tuple[VGroup, VGroup]:
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
        total_width = x_end - x_start

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
        self.play(Write(formulas))

        approx_value = MathTex(
            r"\int_{-2}^{2} f(x) \, dx", font_size=36, color=YELLOW
        )
        approx_value.to_edge(RIGHT).shift(DOWN * 2.25 + LEFT)
        self.play(Write(approx_value))

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
        self.add(integral_value)

        prev_rectangles = None
        prev_dots = None

        for step in range(iteration_count):
            integral_value.become(MathTex("", font_size=48, color=YELLOW))

            subinterval_count = 2 ** step
            subinterval_width = total_width / subinterval_count
            subinterval_bounds = [
                x_start + i * subinterval_width for i in range(subinterval_count + 1)
            ]

            subinterval_rects = VGroup()
            dot_group = VGroup()
            accumulated_area = 0

            for i in range(subinterval_count):
                x_left = subinterval_bounds[i]
                x_right = subinterval_bounds[i + 1]
                x_mid = (x_left + x_right) / 2
                height = integrand(x_mid)

                # 점 추가 (높이에 상관없이 동일한 색상)
                dot = Dot(
                    point=self.plane.c2p(x_mid, height),
                    color=PINK,
                    radius=0.05
                ).set_z_index(10)
                dot_group.add(dot)

                rect = Rectangle(
                    width=subinterval_width,
                    height=abs(height),
                    fill_opacity=0.3,
                    stroke_width=1,
                    # 높이에 따라 다른 색상 적용
                    color=BLUE if height >= 0 else "#FF69B4"  # BLUE 또는 HOT_PINK
                )

                if height >= 0:
                    rect.move_to(self.plane.c2p(x_mid, 0), aligned_edge=DOWN)
                else:
                    rect.move_to(self.plane.c2p(x_mid, 0), aligned_edge=UP)

                subinterval_rects.add(rect)
                accumulated_area += height * subinterval_width

            formatted_area = f"{accumulated_area:.6f}".rstrip('0').rstrip('.')
            formatted_dx = f"{subinterval_width:.6f}".rstrip('0').rstrip('.')

            # n값 업데이트 (이터레이션 텍스트만)
            if prev_rectangles:
                self.play(
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
                self.play(FadeIn(iter_info_text))

            # 사각형과 점들 생성
            self.play(Create(subinterval_rects), Create(dot_group))

            # 적분값 업데이트 (오른쪽 중앙)
            integral_value.become(
                MathTex(f"\\approx {formatted_area}",
                        font_size=36, color=YELLOW)
            ).next_to(approx_value, DOWN, buff=0.25).shift(RIGHT * 0.5)

            prev_rectangles = subinterval_rects
            prev_dots = dot_group
            self.wait()

        # 마지막 상태 처리
        if remove_after:
            self.play(
                FadeOut(prev_rectangles),
                FadeOut(prev_dots),  # 점들도 함께 제거
                FadeOut(iter_info_text),
                FadeOut(integral_value),
                FadeOut(formulas)  # 상단의 수식들도 함께 제거
            )
            self.wait()
            return None, None

        return prev_rectangles, iter_info_text

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
            "Calculating the Definite Integration Value by Midpoint Riemann Sum")

        self._visualize_riemann_sum(
            f,
            (-2, 2),
            iteration_count=6,
            remove_after=False
        )

        self.wait(2)
