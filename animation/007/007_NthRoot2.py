from manim import *

from common.tex_builder import TexBuilder
from common.manim_utils import create_vertical_dash, format_number


# NOTE: 'NumberPlane'의 x축과 y축의 스케일이 다를때 화면에 표시되는 내용의 '왜곡'이 있을 수 있으니 주의할 것. 잘못된 것이 아닌데 오류라고 생각할 수도 있음.

class NthRootByGradientDescent(Scene):
    def setup(self):
        super().setup()
        self.tex_builder = TexBuilder()
        self.arrow_length = 1
        self.learning_rate = 0.05  # 학습률을 0.05로 변경

    def calculate_next_x(self, current_x, learning_rate):
        """실제 gradient descent 계산"""
        gradient = 4 * current_x * (current_x**2 - 2)
        return current_x - learning_rate * gradient

    def create_gradient_descent_arrow(self, plane, current_x, learning_rate):
        """그래디언트 디센트 화살표 생성"""
        # 현재 위치의 함수값
        start_x = current_x
        start_y = (current_x**2 - 2)**2

        # 다음 위치 계산
        gradient_slope = 4 * current_x * (current_x**2 - 2)
        def tangent_line_y(x): return gradient_slope * \
            (x - current_x) + start_y

        # end_x = self.calculate_next_x(current_x, learning_rate)
        # end_y = tangent_line_y(end_x)

        theta = np.arctan(gradient_slope)
        end_x = current_x + self.arrow_length * np.cos(theta)
        end_y = start_y + self.arrow_length * np.sin(theta)

        return Arrow(
            plane.c2p(start_x, start_y),  # 현재 곡선 위의 점
            plane.c2p(end_x, end_y),      # 다음 곡선 위의 점
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

    def create_tangent_arrow(self, plane, x, length=0.5):
        """특정 지점에서의 접선 방향 화살표 생성"""
        current_y = (x**2 - 2)**2
        gradient = 4 * x * (x**2 - 2)

        start_point = plane.c2p(x, current_y)
        end_x = x + length
        end_y = current_y + gradient * length
        end_point = plane.c2p(end_x, end_y)

        return Arrow(
            start_point,
            end_point,
            color=RED,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )

    def create_gradient_descent_path(self, plane, start_x, end_x):
        """그래디언트 디센트 경로를 따라가는 점의 경로 생성"""
        path = VMobject()
        path.set_points([
            plane.c2p(t, (t**2 - 2)**2)
            for t in np.linspace(start_x, end_x, 100)
        ])
        return path

    def update_gradient_arrow(self, arrow, x, current_x, next_x, alpha, plane):
        """Update arrow position and direction based on current gradient"""
        x = current_x + (next_x - current_x) * alpha
        current_y = (x**2 - 2)**2
        gradient = 4 * x * (x**2 - 2)

        # 기울기를 이용해 각도 계산
        theta = np.arctan(gradient)  # 기울기의 각도

        start_point = plane.c2p(x, current_y)
        # 항상 일정한 길이의 화살표를 각도에 따라 계산
        end_x = x + self.arrow_length * np.cos(theta)
        end_y = current_y + self.arrow_length * np.sin(theta)
        end_point = plane.c2p(end_x, end_y)

        arrow.put_start_and_end_on(start_point, end_point)

    def construct(self):
        tb = self.tex_builder

        self.next_section(
            "Gradient Descent Method Formular Derivation", skip_animations=True)

        # 타이틀
        title_parts = [
            r"\text{Gradient Descent Method: Finding }",
            (r"\sqrt{2}", GREEN)
        ]
        title = tb.create_colored_tex(title_parts)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # 수식과 설명을 포함한 테이블 생성
        contents = [
            ([("x^2 = 2", GREEN)], "Target equation"),
            ([("f(x)", BLUE), " = (x^2 - 2)^2"], "Loss function (squared error)"),
            ([("f'(x)", RED), " = 4x(x^2-2)"], "Gradient of loss function"),
            (["x_{n+1} = x_n - \\alpha", ("f'(x_n)", RED)],
             "Gradient descent update rule"),
            (["x_{n+1} = x_n - \\alpha \\cdot 4x_n(x_n^2-2)"],
             "Substituted gradient"),
            (["\\alpha = 0.05"], "Learning rate (step size)"),  # 학습률 표시 변경
            ([(r"x_{n+1} = x_n - 0.2x_n(x_n^2-2)", GREEN)],   # 수식도 변경
             "Final update formula")
        ]

        table = tb.create_equation_table(
            contents, description_color=GRAY_C, v_buff=0.5)
        table.scale(0.8)
        table.next_to(title, DOWN, buff=0.5)

        self.play(Create(table), run_time=0.5 * len(contents))
        self.wait(2)

        # 마지막 수식을 테이블에서 복제하여 화면 좌상단으로 이동
        last_equation = table.get_entries(pos=(7, 1))[-1].copy()
        self.play(
            last_equation.animate.to_edge(UR).set_z_index(9999),
            FadeOut(title),
            FadeOut(table)
        )

        self.next_section("Target Equation", skip_animations=True)

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
            UL).shift(RIGHT * 3).set_z_index(9999)

        start_group = VGroup(start_plane, start_dot,
                             start_graph, start_graph_label)
        self.play(FadeIn(start_group))
        self.play(FadeOut(start_graph_label))
        start_group.remove(start_graph_label)

        self.next_section("Loss Function", skip_animations=True)

        mid_plane = NumberPlane(
            x_range=[-2, 8],
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
            lambda x: (x**2 - 2)**2,
            x_range=[-2, 3],
            color=YELLOW
        )

        graph_label = MathTex(
            "y = (x^2 - 2)^2").shift(DOWN * 2 + LEFT * 3).set_z_index(9999)
        end_group = VGroup(mid_plane, origin_dot, graph)
        self.play(ReplacementTransform(start_group, end_group))
        self.play(FadeIn(graph_label))

        # Learning rate (step size) 추가
        alpha = MathTex(r"\alpha = ", str(self.learning_rate), color=GRAY).next_to(
            last_equation, DOWN, buff=0.2).set_z_index(9999)

        # Add iteration 1 indicator (WHITE 색상으로 변경)
        iter_text = MathTex("\\text{Step 1}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(FadeIn(alpha), FadeIn(iter_text))
        self.play(FadeOut(graph_label))

        x0_value = 2
        x1_value = self.calculate_next_x(x0_value, self.learning_rate)
        x2_value = self.calculate_next_x(x1_value, self.learning_rate)
        x3_value = self.calculate_next_x(x2_value, self.learning_rate)
        x4_value = self.calculate_next_x(x3_value, self.learning_rate)

        # 시작점 x₀ = 2 설정
        x0 = MathTex("x_0 = 2", color=GRAY).to_edge(UP).shift(
            DOWN * 1.3 + RIGHT * 1.5).set_z_index(9999)
        self.play(FadeIn(x0), run_time=0.5)

        self.next_section("Gradient Descent Step 1", skip_animations=False)

        x1 = MathTex("x_1 = ", format_number(x1_value), color=GRAY).next_to(
            x0, DOWN, buff=0.2).set_z_index(9999)
        x1_value_dot = Dot(mid_plane.c2p(x1_value, 0),
                           color=GREEN,
                           radius=DEFAULT_DOT_RADIUS * 0.7
                           )
        self.play(
            FadeIn(create_vertical_dash(mid_plane, x1_value)),
            FadeIn(x1),
            FadeIn(x1_value_dot),
            run_time=0.5
        )

        x1_gradient_arrow_start_dot = Dot(
            mid_plane.c2p(x1_value, (x1_value**2 - 2)**2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        x1_gradient_arrow = self.create_gradient_descent_arrow(
            mid_plane, x1_value, self.learning_rate)
        self.play(FadeIn(x1_gradient_arrow_start_dot), run_time=0.5)
        self.play(FadeIn(x1_gradient_arrow), run_time=0.5)

        self.play(Transform(iter_text, MathTex(
            "\\text{Step 2}", color=WHITE).to_edge(UP).set_z_index(9999)))

        x2 = MathTex("x_2 = ", format_number(x2_value), color=GRAY).next_to(
            x1, DOWN, buff=0.2).set_z_index(9999)
        x2_value_dot = Dot(mid_plane.c2p(x2_value, 0),
                           color=GREEN,
                           radius=DEFAULT_DOT_RADIUS * 0.7
                           )
        self.play(
            FadeIn(create_vertical_dash(mid_plane, x2_value)),
            FadeIn(x2),
            FadeIn(x2_value_dot),
            run_time=0.5
        )

        # x1에서 x2로 이동하는 애니메이션
        moving_dot = Dot(
            mid_plane.c2p(x1_value, (x1_value**2 - 2)**2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        descent_path = self.create_gradient_descent_path(
            mid_plane, x1_value, x2_value)

        self.play(
            MoveAlongPath(moving_dot, descent_path),
            UpdateFromAlphaFunc(
                x1_gradient_arrow,
                lambda arrow, alpha: self.update_gradient_arrow(
                    arrow, x1_value, x1_value, x2_value, alpha, mid_plane)
            )
        )

        self.next_section("Gradient Descent Step 2", skip_animations=False)

        x2_gradient_arrow_start_dot = Dot(
            mid_plane.c2p(x2_value, (x2_value**2 - 2)**2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        x2_gradient_arrow = self.create_gradient_descent_arrow(
            mid_plane, x2_value, self.learning_rate)
        self.add(x2_gradient_arrow_start_dot)
        self.add(x2_gradient_arrow)

        self.play(Transform(iter_text, MathTex(
            "\\text{Step 3}", color=WHITE).to_edge(UP).set_z_index(9999)))

        # NOTE: 3단계에서 구한 값은 소수점 아래 5자리를 초과한 값이 나와서 화면상에서는 반올림하여 표시된다.
        x3 = MathTex(r"x_3 \approx ", format_number(x3_value), color=GRAY).next_to(
            x2, DOWN, buff=0.2).set_z_index(9999)
        x3_value_dot = Dot(mid_plane.c2p(x3_value, 0),
                           color=GREEN,
                           radius=DEFAULT_DOT_RADIUS * 0.7
                           )
        self.play(
            FadeIn(create_vertical_dash(mid_plane, x3_value)),
            FadeIn(x3),
            FadeIn(x3_value_dot),
            run_time=0.5
        )

        # x2에서 x3로 이동하는 애니메이션
        moving_dot = Dot(
            mid_plane.c2p(x2_value, (x2_value**2 - 2)**2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        descent_path = self.create_gradient_descent_path(
            mid_plane, x2_value, x3_value)

        self.remove(x1_gradient_arrow)
        self.play(
            MoveAlongPath(moving_dot, descent_path),
            UpdateFromAlphaFunc(
                x2_gradient_arrow,
                lambda arrow, alpha: self.update_gradient_arrow(
                    arrow, x2_value, x2_value, x3_value, alpha, mid_plane)
            )
        )

        self.next_section("Gradient Descent Step 3", skip_animations=False)

        x3_gradient_arrow_start_dot = Dot(
            mid_plane.c2p(x3_value, (x3_value**2 - 2)**2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        x3_gradient_arrow = self.create_gradient_descent_arrow(
            mid_plane, x3_value, self.learning_rate)
        self.add(x3_gradient_arrow_start_dot)
        self.add(x3_gradient_arrow)

        self.play(Transform(iter_text, MathTex(
            "\\text{Step 4}", color=WHITE).to_edge(UP).set_z_index(9999)))

        x4 = MathTex(r"x_4 \approx ", format_number(x4_value), color=GRAY).next_to(
            x3, DOWN, buff=0.2).set_z_index(9999)
        x4_value_dot = Dot(mid_plane.c2p(x4_value, 0),
                           color=GREEN,
                           radius=DEFAULT_DOT_RADIUS * 0.7
                           )
        self.play(
            FadeIn(create_vertical_dash(mid_plane, x4_value)),
            FadeIn(x4),
            FadeIn(x4_value_dot),
            run_time=0.5
        )

        # x3에서 x4로 이동하는 애니메이션
        moving_dot = Dot(
            mid_plane.c2p(x3_value, (x3_value**2 - 2)**2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        descent_path = self.create_gradient_descent_path(
            mid_plane, x3_value, x4_value)

        self.remove(x2_gradient_arrow)
        self.play(
            MoveAlongPath(moving_dot, descent_path),
            UpdateFromAlphaFunc(
                x3_gradient_arrow,
                lambda arrow, alpha: self.update_gradient_arrow(
                    arrow, x3_value, x3_value, x4_value, alpha, mid_plane)
            )
        )
        self.play(x4.animate.set_color(GREEN))

        self.wait(2)
