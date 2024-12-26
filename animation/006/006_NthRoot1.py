from manim import *

from common.tex_builder import TexBuilder
from common.manim_utils import create_vertical_dash, format_number


class NthRootByNewtonRaphson(Scene):
    def setup(self):
        super().setup()
        self.tex_builder = TexBuilder()

    def construct(self):
        tb = self.tex_builder

        self.next_section("Newton-Raphson Method Formular Derivation")

        # 타이틀
        title_parts = [
            r"\text{Newton-Raphson Method: Finding }",
            (r"\sqrt{2}", GREEN)
        ]
        title = tb.create_colored_tex(title_parts)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # 수식과 설명을 포함한 테이블 생성
        contents = [
            ([("x^2 = 2", GREEN)], "Given equation"),
            ([("f(x)", BLUE), " = x^2 - 2"], "Convert to function form"),
            ([("f'(x)", RED), " = 2x"], "Derivative of function"),
            (["x_{n+1} = x_n - {", ("f(x_n)", BLUE), "\over", ("f'(x_n)", RED), "}"],
             "Newton-Raphson formula"),
            ([(r"x_{n+1} = x_n - \frac{x_n^2 - 2}{2x_n}", WHITE)],
             "Simplified formula"),
            ([(r"x_{n+1} = \frac{x_n}{2} + \frac{1}{x_n}", GREEN)], None)
        ]

        table = tb.create_equation_table(
            contents, description_color=GRAY_C, v_buff=0.5)  # 설명 텍스트 색상을 회색으로 변경
        table.scale(0.8)
        table.next_to(title, DOWN, buff=0.5)

        self.play(Create(table), run_time=0.5 * len(contents))
        self.wait(2)

        # 마지막 수식을 테이블에서 복제하여 화면 좌상단으로 이동
        last_equation = table.get_entries(pos=(5, 1))[-1].copy()
        self.play(
            last_equation.animate.to_edge(UP + LEFT).set_z_index(9999),
            FadeOut(title),
            FadeOut(table)
        )

        self.next_section("Newton-Raphson Method Visualization")

        # 초기 상태 (전체 화면)
        start_plane = NumberPlane(
            x_range=[-8, 8],
            y_range=[-4, 4],
            x_length=16,
            y_length=8,
            background_line_style={
                "stroke_opacity": 0.0  # ��음에는 완전 투명
            },
            axis_config={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "unit_size": 1.0
            }
        )

        # start_plane용 원점과 그래프
        start_dot = Dot(
            start_plane.c2p(0, 0),
            color=BLUE,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        start_graph = start_plane.plot(
            lambda x: x**2,
            x_range=[-3, 3],  # 전체 화면에 맞는 더 넓은 범위
            color=TEAL_E
        )
        start_graph_label = MathTex("y = x^2").to_edge(
            UP).shift(RIGHT * 3).set_z_index(9999)

        start_group = VGroup(start_plane, start_dot,
                             start_graph, start_graph_label)
        self.play(FadeIn(start_group))
        self.play(FadeOut(start_graph_label))
        start_group.remove(start_graph_label)

        mid_plane = NumberPlane(
            x_range=[-2, 4],
            y_range=[-3, 5],  # y축 범위를 1만큼 아래로
            x_length=16,
            y_length=8,
            background_line_style={
                "stroke_opacity": 0.25
            },
            axis_config={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "unit_size": 1.0
            }
        )

        # 원점 점과 그래프는 mid_plane 기준으로 생성
        origin_dot = Dot(
            mid_plane.c2p(0, 0),
            color=BLUE,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        graph = mid_plane.plot(
            lambda x: x**2 - 2,  # y = x² - 2로 변경
            x_range=[-2, 3],
            color=YELLOW
        )

        graph_label = MathTex(
            "y = x^2 - 2").to_edge(UP + RIGHT).set_z_index(9999)
        end_group = VGroup(mid_plane, origin_dot, graph)
        self.play(ReplacementTransform(start_group, end_group))
        self.play(FadeIn(graph_label))

        x0 = MathTex("x_0 = 2").next_to(
            last_equation, DOWN, buff=0.2).set_z_index(9999)

        # Add iteration 1 indicator (WHITE 색상으로 변경)
        iter_text = MathTex("\\text{Iteration 1}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(FadeIn(x0), FadeIn(iter_text))
        self.play(FadeOut(graph_label))

        # Iteration 1: Add vertical dash at x=2 before tangent line
        x_value = 2
        vertical_dash = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash), run_time=0.5)

        # Add tangent line at x=2
        x_value = 2
        slope = 2 * x_value  # derivative of y = x^2 - 2 at x=2
        tangent_line = mid_plane.plot(
            lambda x: slope * (x - x_value) + (x_value**2 - 2),
            x_range=[x_value - 3, x_value + 3],
            color=RED
        )
        tangent_dot = Dot(
            mid_plane.c2p(x_value, x_value**2 - 2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        self.play(Create(tangent_line), FadeIn(tangent_dot))

        # Add dot at intersection of tangent line and x-axis
        intersection_x = x_value - (x_value**2 - 2) / slope
        intersection_dot = Dot(
            mid_plane.c2p(intersection_x, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        self.play(FadeIn(intersection_dot))

        # Add arrow pointing to the intersection point from bottom-right diagonal
        arrow = Arrow(
            start=mid_plane.c2p(intersection_x + 0.4, -0.7),
            end=mid_plane.c2p(intersection_x + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(FadeIn(arrow), run_time=0.5)

        # Add x-value of the intersection point near the arrow's starting point
        intersection_x_value = MathTex(
            format_number(intersection_x))
        intersection_x_value.next_to(
            arrow.get_start(), RIGHT, buff=0.1).shift(DOWN * 0.1)
        self.play(FadeIn(intersection_x_value))

        # Transform the number plane to show x-axis range from 0 to 3
        final_plane = NumberPlane(
            x_range=[0, 3],
            y_range=[-2, 4],
            x_length=16,
            y_length=8,
            background_line_style={
                "stroke_opacity": 0.25
            },
            axis_config={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "unit_size": 1.0
            }
        )

        final_graph = final_plane.plot(
            lambda x: x**2 - 2,
            x_range=[0, 3],
            color=YELLOW
        )

        # final_plane용 원점 추가
        final_origin_dot = Dot(
            final_plane.c2p(0, 0),
            color=BLUE,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        final_group = VGroup(final_plane, final_origin_dot, final_graph)

        # x1 값 미리 생성
        x1 = MathTex(f"x_1 = {format_number(intersection_x)}").next_to(
            x0, DOWN, buff=0.2).set_z_index(9999)

        # final_plane 전환과 함께 intersection_x_value를 x1으로 transform
        # Iteration 2 (WHITE 색상으로 변경)
        iter_text_2 = MathTex("\\text{Iteration 2}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            FadeOut(arrow),
            FadeOut(intersection_dot),
            FadeOut(tangent_line),
            FadeOut(tangent_dot),
            ReplacementTransform(end_group, final_group),
            ReplacementTransform(intersection_x_value, x1),
            ReplacementTransform(iter_text, iter_text_2)
        )

        # Iteration 2: Add vertical dash at x=intersection_x before tangent line
        x_value = intersection_x
        vertical_dash_2 = create_vertical_dash(final_plane, x_value)
        self.play(Create(vertical_dash_2), run_time=0.5)

        # Add new tangent line at x=x1
        x_value = intersection_x  # 이전에 구한 x1 값 사용
        slope = 2 * x_value  # derivative of y = x^2 - 2 at x=x1
        tangent_line = final_plane.plot(
            lambda x: slope * (x - x_value) + (x_value**2 - 2),
            x_range=[x_value - 1, x_value + 1],
            color=RED
        )
        tangent_dot = Dot(
            final_plane.c2p(x_value, x_value**2 - 2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        self.play(Create(tangent_line), FadeIn(tangent_dot))

        # Add dot at new intersection point
        intersection_x = x_value - (x_value**2 - 2) / slope
        intersection_dot = Dot(
            final_plane.c2p(intersection_x, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        self.play(FadeIn(intersection_dot))

        # Add new arrow pointing to the intersection point
        arrow = Arrow(
            start=final_plane.c2p(intersection_x + 0.4, -0.7),
            end=final_plane.c2p(intersection_x + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(FadeIn(arrow), run_time=0.5)

        # Add new intersection x-value
        intersection_x_value = MathTex(
            format_number(intersection_x)
        )
        intersection_x_value.next_to(
            arrow.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)
        self.play(FadeIn(intersection_x_value))

        # x2를 위한 다음 이터레이션
        # x2 값 미리 생���
        x2 = MathTex(f"x_2 = {format_number(intersection_x)}").next_to(
            x1, DOWN, buff=0.2).set_z_index(9999)

        # 이전 이터레이션의 요소들을 페이드아웃하면서 x2로 트랜스폼
        # Iteration 3 (WHITE 색상으로 변경)
        iter_text_3 = MathTex("\\text{Iteration 3}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            FadeOut(arrow),
            FadeOut(intersection_dot),
            FadeOut(tangent_line),
            FadeOut(tangent_dot),
            ReplacementTransform(intersection_x_value, x2),
            ReplacementTransform(iter_text_2, iter_text_3)
        )

        # Iteration 3: Add vertical dash at x=intersection_x before tangent line
        x_value = intersection_x
        vertical_dash_3 = create_vertical_dash(final_plane, x_value)
        self.play(Create(vertical_dash_3), run_time=0.5)

        # Add final iteration's tangent line at x=x2
        x_value = intersection_x
        slope = 2 * x_value
        tangent_line = final_plane.plot(
            lambda x: slope * (x - x_value) + (x_value**2 - 2),
            x_range=[x_value - 0.5, x_value + 0.5],
            color=RED
        )
        tangent_dot = Dot(
            final_plane.c2p(x_value, x_value**2 - 2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        self.play(Create(tangent_line), FadeIn(tangent_dot))

        # Add dot at final intersection point
        intersection_x = x_value - (x_value**2 - 2) / slope
        intersection_dot = Dot(
            final_plane.c2p(intersection_x, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        self.play(FadeIn(intersection_dot))

        # Add final arrow
        arrow = Arrow(
            start=final_plane.c2p(intersection_x + 0.4, -0.7),
            end=final_plane.c2p(intersection_x + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(FadeIn(arrow), run_time=0.5)

        # Add final x-value
        intersection_x_value = MathTex(
            format_number(intersection_x)
        )
        intersection_x_value.next_to(
            arrow.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)
        self.play(FadeIn(intersection_x_value))

        # Create x3 as a single MathTex and animate its movement
        x3 = MathTex(
            f"x_3 = {format_number(intersection_x)}"
        ).set_color(GREEN).set_weight(BOLD)
        x3.next_to(x2, DOWN, buff=0.2).set_z_index(9999)

        # After final intersection is found, add last vertical dash
        vertical_dash_4 = create_vertical_dash(
            final_plane, intersection_x, color=GREEN, opacity=0.5)
        self.play(
            FadeIn(vertical_dash_4),
            TransformFromCopy(intersection_x_value, x3),
            run_time=1.5
        )

        # 마지막에 iteration 텍스트 제거하고 수렴 메시지 표시
        convergence_text = MathTex(
            "\\text{Converged to 4 decimal places: }",
            f"{format_number(intersection_x, 4)}",
            "\\approx \\sqrt{2}"
        ).set_color(GREEN)
        convergence_text.to_edge(UR).set_z_index(9999)

        self.play(
            FadeOut(iter_text_3),
            final_group.animate.set_opacity(0.2).set_fill(opacity=0),
            vertical_dash.animate.set_opacity(0.1),
            vertical_dash_2.animate.set_opacity(0.1),
            vertical_dash_3.animate.set_opacity(0.1),
            vertical_dash_4.animate.set_opacity(0.3),
            FadeIn(convergence_text),
            run_time=2.5
        )

        self.wait(2)
