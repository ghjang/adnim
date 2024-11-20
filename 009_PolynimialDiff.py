from manim import *
from sympy import symbols, diff, solve, latex
from lib.manim_utils import create_code_block_from_file


class PolynimialDiff(Scene):
    def construct(self):
        self.next_section("Display Code Block")

        code_block = create_code_block_from_file(
            "009_sympy_snippet.py",
            style="monokai",  # theme 대신 style 사용
        ).scale(0.8).to_edge(UP)
        code_block_label = Text(
            """You can use SymPy module to perform
symbolic mathematics operations
like differentiation and equation solving."""
        ).next_to(code_block, DOWN).align_to(code_block, LEFT)
        code_block_group = VGroup(code_block, code_block_label)
        self.add(code_block_group)
        self.wait(2)
        self.remove(code_block_group)

        self.next_section("Differentiate Polynomial and Solve")

        # Define the symbol x
        x = symbols('x')

        # Define the polynomial expression
        poly_expr = x**3 - 4*x**2 + 3*x + 5

        # Differentiate the polynomial expression
        diff_expr = diff(poly_expr, x)

        # Convert the polynomial and its derivative to LaTeX format
        poly_expr_tex = MathTex(
            "f(x)", "=", latex(poly_expr)
        ).scale(1.25).to_edge(UP)
        poly_expr_tex[0].set_color(BLUE)  # f(x) 부분만 파란색으로

        diff_expr_tex = MathTex(
            "f'(x)", "=", latex(diff_expr)
        ).scale(1.25).next_to(poly_expr_tex, DOWN).shift(DOWN)
        diff_expr_tex[0].set_color(RED)  # f'(x) 부분만 빨간색으로

        # Display the polynomial and its derivative on the screen
        self.play(FadeIn(poly_expr_tex))
        self.play(FadeIn(diff_expr_tex))

        # Create a 2x2 grid for solutions
        solution_grid = VGroup()
        grid_eq = MathTex("f'(x)", "= 0,").scale(1.25)
        grid_eq[0].set_color(RED)  # f'(x) 부분만 빨간색으로
        grid_empty = MathTex("")  # 빈 셀 추가

        # Solve the differentiated expression for x
        diff_expr_solution = solve(diff_expr, x)
        grid_sol1 = MathTex(
            "x", "=", latex(diff_expr_solution[0])
        ).scale(1.25)
        grid_sol1[0].set_color(GREEN)  # x를 녹색으로

        grid_sol2 = MathTex(
            "x", "=", latex(diff_expr_solution[1])
        ).scale(1.25)
        grid_sol2[0].set_color(GREEN)  # x를 녹색으로

        # Arrange in 2x2 grid
        solution_grid = VGroup(
            grid_eq, grid_sol1,
            grid_empty, grid_sol2
        ).arrange_in_grid(rows=2, cols=2, buff=0.5)

        solution_grid.next_to(diff_expr_tex, DOWN, buff=1)

        # Animate the grid appearing
        self.play(FadeIn(solution_grid))
        self.wait(2)

        # Hide all previous content
        self.play(
            FadeOut(poly_expr_tex),
            FadeOut(diff_expr_tex),
            FadeOut(solution_grid)
        )

        self.next_section("Graphs of Polynomial and Derivative")

        # Create number plane instead of axes
        plane = NumberPlane(
            x_range=[-3, 5],
            y_range=[-3, 7],
            x_length=16,
            y_length=8,
            background_line_style={
                "stroke_opacity": 0.5
            }
        )

        # Add origin dot
        origin_dot = Dot(
            point=plane.c2p(0, 0),
            color=WHITE,
            radius=0.05
        )

        # Convert sympy expression to lambda function for plotting
        def f(x_val):
            return float(poly_expr.subs(x, x_val))  # x 심볼로 대체

        # Create graph of original function
        graph = plane.plot(
            function=f,
            x_range=[-2, 4],  # 적절한 x 범위 설정
            use_smoothing=True,
            color=BLUE
        )

        # Convert derivative expression to function for plotting
        def df(x_val):
            return float(diff_expr.subs(x, x_val))

        # Create graph of derivative function
        derivative_graph = plane.plot(
            function=df,
            x_range=[-2, 4],
            use_smoothing=True,
            color=RED
        )

        plane_group = VGroup(plane, origin_dot)

        # Center the entire visualization
        graph_group = VGroup(plane_group, graph, derivative_graph)

        # Create function labels
        f_label = MathTex("f(x)").set_color(BLUE).scale(1.2)
        f_label.to_edge(RIGHT).shift(UP * 3 + LEFT)

        df_label = MathTex("f'(x)").set_color(RED).scale(1.2)
        df_label.to_edge(DOWN).shift(UP * 0.5 + RIGHT * 3)

        # Animate in sequence
        self.play(FadeIn(plane_group))
        self.play(Create(graph))
        self.play(Write(f_label))
        self.wait()
        self.play(FadeOut(f_label))

        self.play(Create(derivative_graph))
        self.play(Write(df_label))
        self.play(FadeOut(df_label))

        self.next_section("Add Vertical Solution Lines")

        # Create vertical lines at solution points
        v_lines = VGroup()
        x_dots = VGroup()  # 점들을 담을 그룹 추가

        for sol in diff_expr_solution:
            x_val = float(sol)
            # 수직 점선 생성
            v_line = DashedLine(
                start=plane.c2p(x_val, plane.y_range[0]),
                end=plane.c2p(x_val, plane.y_range[1]),
                color=GREEN,
                stroke_width=2,
                dash_length=0.2
            )
            v_lines.add(v_line)

            # x축 상의 점 생성
            x_dot = Dot(
                point=plane.c2p(x_val, 0),
                color=GREEN,
                radius=0.05
            )
            x_dots.add(x_dot)

        # Animate vertical lines and dots
        for line, dot in zip(v_lines, x_dots):
            self.play(
                Create(line),
                FadeIn(dot),
                run_time=0.5
            )

        self.wait(1)

        self.next_section("Add Tangent Lines at Solution Points")

        # Fade out derivative graph and vertical lines more dramatically
        self.play(
            derivative_graph.animate.set_opacity(0.15).set_fill(opacity=0),
            v_lines.animate.set_opacity(0.5),
            x_dots.animate.set_opacity(0.5),
            run_time=1
        )

        # Create tangent lines and points at solution points
        tangent_lines = VGroup()
        tangent_points = VGroup()  # 접점들을 담을 그룹 추가

        for sol in diff_expr_solution:
            x_val = float(sol)
            y_val = f(x_val)  # 원함수의 y값

            # 접점에 점 생성
            point_dot = Dot(
                point=plane.c2p(x_val, y_val),
                color=YELLOW,
                radius=0.05
            )
            tangent_points.add(point_dot)

            # 접선의 기울기는 0 (도함수의 근이므로)
            tangent_line = Line(
                start=plane.c2p(x_val - 1, y_val),
                end=plane.c2p(x_val + 1, y_val),
                color=YELLOW,
                stroke_width=2
            )
            tangent_lines.add(tangent_line)

        # Animate tangent lines and points
        for line, point in zip(tangent_lines, tangent_points):
            self.play(
                Create(line),
                FadeIn(point),
                run_time=0.8
            )

        self.wait(1)

        self.next_section("Add Sliding Tangent Line")

        # Fade out previous tangent lines and points
        self.play(
            tangent_lines.animate.set_opacity(0.3),
            tangent_points.animate.set_opacity(0.3),
            run_time=0.5
        )

        # Get the range between two solutions
        x_start = float(min(diff_expr_solution))
        x_end = float(max(diff_expr_solution))

        # Create sliding dot and tangent line
        sliding_dot = Dot(
            point=plane.c2p(x_start, f(x_start)),
            color=GOLD_E,
            radius=0.075
        ).set_z_index(9999)

        def get_tangent_line(x):
            slope = df(x)  # 도함수 값이 접선의 기울기
            y = f(x)
            p1 = plane.c2p(x - 0.5, y - 0.5 * slope)
            p2 = plane.c2p(x + 0.5, y + 0.5 * slope)
            return Line(p1, p2, color=YELLOW_E, stroke_width=4)

        # Initial tangent line
        sliding_line = get_tangent_line(x_start)

        self.play(
            FadeIn(sliding_dot),
            Create(sliding_line)
        )

        # Animate the sliding motion
        def update_dot(mob, alpha):
            x = x_start + (x_end - x_start) * alpha
            y = f(x)
            mob.move_to(plane.c2p(x, y))

        def update_line(mob, alpha):
            x = x_start + (x_end - x_start) * alpha
            new_line = get_tangent_line(x)
            mob.become(new_line)

        self.play(
            UpdateFromAlphaFunc(sliding_dot, update_dot),
            UpdateFromAlphaFunc(sliding_line, update_line),
            run_time=3,
            rate_func=linear
        )

        self.wait(2)
