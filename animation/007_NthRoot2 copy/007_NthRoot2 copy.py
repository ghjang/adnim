from manim import *
from common.tex_builder import TexBuilder
from common.manim_utils import create_vertical_dash, format_number


class NthRootByGradientDescent(Scene):
    def setup(self):
        super().setup()
        self.tex_builder = TexBuilder()

    def calculate_next_x(self, current_x, learning_rate):
        """실제 gradient descent 계산"""
        gradient = 4 * current_x * (current_x**2 - 2)
        return current_x - learning_rate * gradient

    def create_gradient_descent_arrow(self, plane, current_x, learning_rate):
        """그래디언트 디센트 화살표 생성"""
        # 현재 위치의 함수값
        current_y = (current_x**2 - 2)**2
        
        # 다음 위치 계산
        new_x = self.calculate_next_x(current_x, learning_rate)
        new_y = (new_x**2 - 2)**2  # 다음 위치의 실제 함수값
        
        return Arrow(
            plane.c2p(current_x, current_y),  # 현재 곡선 위의 점
            plane.c2p(new_x, new_y),         # 다음 곡선 위의 점
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        ), new_x

    def construct(self):
        tb = self.tex_builder

        self.next_section("Gradient Descent Method Formular Derivation")

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
            (["\\alpha = 0.1"], "Learning rate (step size)"),
            ([(r"x_{n+1} = x_n - 0.4x_n(x_n^2-2)", GREEN)],
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
            last_equation.animate.to_edge(DL).shift(UP).set_z_index(9999),
            FadeOut(title),
            FadeOut(table)
        )

        self.next_section("Gradient Descent Method Visualization")

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
            lambda x: (x**2 - 2)**2,
            x_range=[-2, 3],
            color=YELLOW
        )

        graph_label = MathTex("y = (x^2 - 2)^2").to_edge(UR).set_z_index(9999)
        end_group = VGroup(mid_plane, origin_dot, graph)
        self.play(ReplacementTransform(start_group, end_group))
        self.play(FadeIn(graph_label))

        # Learning rate (step size) 추가
        alpha = MathTex(r"\alpha = 0.1").next_to(
            last_equation, DOWN, buff=0.2).set_z_index(9999)

        # Add iteration 1 indicator (WHITE 색상으로 변경)
        iter_text = MathTex("\\text{Step 1}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(FadeIn(alpha), FadeIn(iter_text))
        self.play(FadeOut(graph_label))

        # 시작점 x₀ = 2 설정
        x0 = MathTex("x_0 = 2").to_edge(UR).shift(LEFT).set_z_index(9999)
        self.play(FadeIn(x0))

        # x₀ 위치에 수직선 추가
        x_value = 2
        vertical_dash = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash), run_time=0.5)

        # x₀ 위치에 점 추가
        current_point = Dot(
            mid_plane.c2p(x_value, (x_value**2 - 2)**2),
            color=RED,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )
        self.play(FadeIn(current_point))

        # Gradient 방향 화살표 추가 (접선 형태로 수정)
        x_value = 2
        gradient = 4 * x_value * (x_value**2 - 2)  # f'(x) = 4x(x²-2)
        learning_rate = 0.1

        # 접선의 시작점
        arrow_start = mid_plane.c2p(x_value, (x_value**2 - 2)**2)

        # 접선의 끝점 (x방향으로 learning_rate만큼 이동)
        next_x = x_value - learning_rate
        next_y = (x_value**2 - 2)**2 + gradient * \
            (next_x - x_value)  # 접선 방정식 사용

        arrow_end = mid_plane.c2p(next_x, next_y)
        gradient_arrow = Arrow(
            arrow_start,
            arrow_end,
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(Create(gradient_arrow))

        # 실제 다음 x 위치 계산 (그래디언트 descent)
        new_x = x_value - learning_rate * gradient

        # x축 위의 새로운 위치에 점만 추가 (곡선 위 점은 제거)
        intersection_dot = Dot(
            mid_plane.c2p(new_x, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        # 새로운 위치를 가리키는 화살표
        arrow = Arrow(
            start=mid_plane.c2p(new_x + 0.4, -0.7),
            end=mid_plane.c2p(new_x + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

        # x₁ 값을 화살표 근처에 표시
        intersection_x_value = MathTex(format_number(new_x))
        intersection_x_value.next_to(
            arrow.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)

        # x₁ 값 표시 (방정식 리스트에)
        x1 = MathTex(f"x_1 = {format_number(new_x)}").next_to(
            x0, DOWN, buff=0.2).set_z_index(9999)

        self.play(
            FadeIn(intersection_dot),
            FadeIn(arrow),
            FadeIn(intersection_x_value),
            FadeIn(x1),
            run_time=1
        )

        # 다음 이터레이션을 위한 준비
        iter_text_2 = MathTex("\\text{Step 2}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            FadeOut(arrow),
            FadeOut(intersection_x_value),
            ReplacementTransform(iter_text, iter_text_2)
        )

        # Step 2: x_value - learning_rate
        x_value -= learning_rate
        vertical_dash_2 = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash_2), run_time=0.5)

        # Step 2의 gradient arrow 수정
        gradient = 4 * x_value * (x_value**2 - 2)  # 현재 위치에서의 gradient

        # 접선의 시작점은 현재 위치
        arrow_start = mid_plane.c2p(x_value, (x_value**2 - 2)**2)

        # 접선의 끝점은 x방향으로 learning_rate만큼 이동
        next_x = x_value - learning_rate  # 단순히 learning_rate만큼 x축 방향으로 이동
        next_y = (x_value**2 - 2)**2 + gradient * (next_x - x_value)  # 접선 방정식

        arrow_end = mid_plane.c2p(next_x, next_y)
        gradient_arrow_2 = Arrow(
            arrow_start,
            arrow_end,
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(Create(gradient_arrow_2))

        # 실제 다음 위치 계산 (gradient * learning_rate만큼 이동)
        new_x_2 = x_value - learning_rate * gradient

        # x₂ 위치에서의 교점과 화살표, 수치 (곡선 상의 점은 제거)
        intersection_dot_2 = Dot(
            mid_plane.c2p(new_x_2, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        arrow_2 = Arrow(
            start=mid_plane.c2p(new_x_2 + 0.4, -0.7),
            end=mid_plane.c2p(new_x_2 + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

        intersection_x_value_2 = MathTex(format_number(new_x_2))
        intersection_x_value_2.next_to(
            arrow_2.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)

        # x₂ 방정식 추가
        x2 = MathTex(f"x_2 = {format_number(new_x_2)}").next_to(
            x1, DOWN, buff=0.2).set_z_index(9999)

        self.play(
            FadeIn(intersection_dot_2),
            FadeIn(arrow_2),
            FadeIn(intersection_x_value_2),
            FadeIn(x2),
            run_time=1
        )

        # 다음 이터레이션을 위한 준비
        iter_text_3 = MathTex("\\text{Step 3}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            # gradient_arrow_2는 남겨두기 위해 제거
            FadeOut(arrow_2),
            FadeOut(intersection_x_value_2),
            ReplacementTransform(iter_text_2, iter_text_3)
        )

        # Step 3: 이전 gradient_arrow_2의 끝점 x 위치에서 시작
        x_value = next_x  # 이전 gradient arrow의 끝점 x 좌표 사용
        vertical_dash_3 = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash_3), run_time=0.5)

        # 나머지 코드는 동일...
        gradient = 4 * x_value * (x_value**2 - 2)

        arrow_start = mid_plane.c2p(x_value, (x_value**2 - 2)**2)
        next_x = x_value - learning_rate
        next_y = (x_value**2 - 2)**2 + gradient * (next_x - x_value)

        gradient_arrow_3 = Arrow(
            arrow_start,
            mid_plane.c2p(next_x, next_y),
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(Create(gradient_arrow_3))

        # 실제 다음 위치 계산
        new_x_3 = x_value - learning_rate * gradient

        # x축 위의 점만 표시
        intersection_dot_3 = Dot(
            mid_plane.c2p(new_x_3, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        arrow_3 = Arrow(
            start=mid_plane.c2p(new_x_3 + 0.4, -0.7),
            end=mid_plane.c2p(new_x_3 + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

        intersection_x_value_3 = MathTex(format_number(new_x_3))
        intersection_x_value_3.next_to(
            arrow_3.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)

        x3 = MathTex(f"x_3 = {format_number(new_x_3)}").next_to(
            x2, DOWN, buff=0.2).set_z_index(9999)

        self.play(
            FadeIn(intersection_dot_3),
            FadeIn(arrow_3),
            FadeIn(intersection_x_value_3),
            FadeIn(x3),
            run_time=1
        )

        # 다음 스텝을 위한 준비 (필요한 경우)
        iter_text_4 = MathTex("\\text{Step 4}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            # gradient_arrow_3는 남기고 arrow_3와 intersection_x_value_3만 제거
            FadeOut(arrow_3),
            FadeOut(intersection_x_value_3),
            ReplacementTransform(iter_text_3, iter_text_4)
        )

        # Step 4: 이전 x 위치에서 시작
        x_value = next_x
        vertical_dash_4 = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash_4), run_time=0.5)

        # Gradient arrow 생성
        gradient = 4 * x_value * (x_value**2 - 2)

        arrow_start = mid_plane.c2p(x_value, (x_value**2 - 2)**2)
        next_x = x_value - learning_rate
        next_y = (x_value**2 - 2)**2 + gradient * (next_x - x_value)

        gradient_arrow_4 = Arrow(
            arrow_start,
            mid_plane.c2p(next_x, next_y),
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(Create(gradient_arrow_4))

        # 실제 다음 위치 계산
        new_x_4 = x_value - learning_rate * gradient

        # x축 위의 점만 표시
        intersection_dot_4 = Dot(
            mid_plane.c2p(new_x_4, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        arrow_4 = Arrow(
            start=mid_plane.c2p(new_x_4 + 0.4, -0.7),
            end=mid_plane.c2p(new_x_4 + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

        intersection_x_value_4 = MathTex(format_number(new_x_4))
        intersection_x_value_4.next_to(
            arrow_4.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)

        x4 = MathTex(f"x_4 = {format_number(new_x_4)}").next_to(
            x3, DOWN, buff=0.2).set_z_index(9999)

        self.play(
            FadeIn(intersection_dot_4),
            FadeIn(arrow_4),
            FadeIn(intersection_x_value_4),
            FadeIn(x4),
            run_time=1
        )

        # Step 5 준비 (iter_text_5 변수 추가)
        iter_text_5 = MathTex("\\text{Step 5}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            FadeOut(arrow_4),
            FadeOut(intersection_x_value_4),
            FadeOut(iter_text_4),
            FadeIn(iter_text_5)
        )

        # Step 5: 이전 x 위치에서 시작
        x_value = next_x
        vertical_dash_5 = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash_5), run_time=0.5)

        # Gradient arrow 생성 및 다음 위치 계산
        gradient = 4 * x_value * (x_value**2 - 2)

        arrow_start = mid_plane.c2p(x_value, (x_value**2 - 2)**2)
        next_x = x_value - learning_rate
        next_y = (x_value**2 - 2)**2 + gradient * (next_x - x_value)

        gradient_arrow_5 = Arrow(
            arrow_start,
            mid_plane.c2p(next_x, next_y),
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(Create(gradient_arrow_5))

        # 실제 다음 위치 계산
        new_x_5 = x_value - learning_rate * gradient

        # x축 위의 점만 표시
        intersection_dot_5 = Dot(
            mid_plane.c2p(new_x_5, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        arrow_5 = Arrow(
            start=mid_plane.c2p(new_x_5 + 0.4, -0.7),
            end=mid_plane.c2p(new_x_5 + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

        intersection_x_value_5 = MathTex(format_number(new_x_5))
        intersection_x_value_5.next_to(
            arrow_5.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)

        x5 = MathTex(f"x_5 = {format_number(new_x_5)}").next_to(
            x4, DOWN, buff=0.2).set_z_index(9999)

        self.play(
            FadeIn(intersection_dot_5),
            FadeIn(arrow_5),
            FadeIn(intersection_x_value_5),
            FadeIn(x5),
            run_time=1
        )

        # Step 6 준비 (iter_text_6 변수 추가)
        iter_text_6 = MathTex("\\text{Step 6}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            FadeOut(arrow_5),
            FadeOut(intersection_x_value_5),
            FadeOut(iter_text_5),
            FadeIn(iter_text_6)
        )

        # Step 6: 이전 x 위치에서 시작
        x_value = next_x
        vertical_dash_6 = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash_6), run_time=0.5)

        # Gradient arrow 생성
        gradient = 4 * x_value * (x_value**2 - 2)

        arrow_start = mid_plane.c2p(x_value, (x_value**2 - 2)**2)
        next_x = x_value - learning_rate
        next_y = (x_value**2 - 2)**2 + gradient * (next_x - x_value)

        gradient_arrow_6 = Arrow(
            arrow_start,
            mid_plane.c2p(next_x, next_y),
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(Create(gradient_arrow_6))

        # 실제 다음 위치 계산
        new_x_6 = x_value - learning_rate * gradient

        # x축 위의 점만 표시
        intersection_dot_6 = Dot(
            mid_plane.c2p(new_x_6, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        arrow_6 = Arrow(
            start=mid_plane.c2p(new_x_6 + 0.4, -0.7),
            end=mid_plane.c2p(new_x_6 + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

        intersection_x_value_6 = MathTex(format_number(new_x_6))
        intersection_x_value_6.next_to(
            arrow_6.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)

        x6 = MathTex(f"x_6 = {format_number(new_x_6)}").next_to(
            x5, DOWN, buff=0.2).set_z_index(9999)

        self.play(
            FadeIn(intersection_dot_6),
            FadeIn(arrow_6),
            FadeIn(intersection_x_value_6),
            FadeIn(x6),
            run_time=1
        )

        # Step 7 준비
        iter_text_7 = MathTex("\\text{Step 7}", color=WHITE).to_edge(
            UP).set_z_index(9999)
        self.play(
            # final_convergence_text 제거는 필요 없음 - 아직 생성되지 않았음
            FadeOut(arrow_6),
            FadeOut(intersection_x_value_6),
            FadeOut(iter_text_6),  # 이전 스텝의 텍스트만 제거
            FadeIn(iter_text_7)
        )

        # Step 7: 이전 x 위치에서 시작
        x_value = next_x
        vertical_dash_7 = create_vertical_dash(mid_plane, x_value)
        self.play(Create(vertical_dash_7), run_time=0.5)

        # Gradient arrow 생성
        gradient = 4 * x_value * (x_value**2 - 2)

        arrow_start = mid_plane.c2p(x_value, (x_value**2 - 2)**2)
        next_x = x_value - learning_rate
        next_y = (x_value**2 - 2)**2 + gradient * (next_x - x_value)

        gradient_arrow_7 = Arrow(
            arrow_start,
            mid_plane.c2p(next_x, next_y),
            color=RED,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(Create(gradient_arrow_7))

        # 실제 다음 위치 계산
        new_x_7 = x_value - learning_rate * gradient

        # x축 위의 점만 표시
        intersection_dot_7 = Dot(
            mid_plane.c2p(new_x_7, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        arrow_7 = Arrow(
            start=mid_plane.c2p(new_x_7 + 0.4, -0.7),
            end=mid_plane.c2p(new_x_7 + 0.04, -0.1),
            color=GREEN,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )

        intersection_x_value_7 = MathTex(format_number(new_x_7))
        intersection_x_value_7.next_to(
            arrow_7.get_start(), RIGHT, buff=0.1
        ).shift(DOWN * 0.1)

        x7 = MathTex(f"x_7 = {format_number(new_x_7)}").next_to(
            x6, DOWN, buff=0.2).set_z_index(9999)

        self.play(
            FadeIn(intersection_dot_7),
            FadeIn(arrow_7),
            FadeIn(intersection_x_value_7),
            FadeIn(x7),
            run_time=1
        )

        # 최종 수렴 메시지 (가장 마지막 값으로 업데이트)
        final_convergence_text = MathTex(
            "\\text{Converged to } \\sqrt{2} \\approx",
            format_number(new_x_7, 4),
            color=GREEN
        ).to_edge(UP).set_z_index(9999)

        self.play(
            # 모든 gradient arrow는 남기고 나머지만 제거
            FadeOut(arrow_7),
            FadeOut(intersection_x_value_7),
            FadeOut(iter_text_7),
            FadeIn(final_convergence_text)
        )

        self.wait(2)

        def calculate_next_x(current_x, learning_rate):
            """실제 gradient descent 계산"""
            gradient = 4 * current_x * (current_x**2 - 2)
            return current_x - learning_rate * gradient

        def create_gradient_descent_visualization(self, plane, x_value, learning_rate, step_num):
            """각 스텝의 시각화 요소 생성"""
            # 현재 x 위치의 점과 함수값
            current_y = (x_value**2 - 2)**2
            current_point = Dot(
                plane.c2p(x_value, current_y),
                color=RED,
                radius=DEFAULT_DOT_RADIUS * 0.7
            )

            # 수직선 생성
            vertical_dash = create_vertical_dash(plane, x_value)

            # 그래디언트에 따른 다음 위치 계산
            next_x = calculate_next_x(x_value, learning_rate)
            next_y = (next_x**2 - 2)**2

            # 그래디언트 화살표 생성 (현재 곡선 위치에서 다음 곡선 위치로)
            gradient_arrow = Arrow(
                plane.c2p(x_value, current_y),
                plane.c2p(next_x, next_y),
                color=RED,
                buff=0,
                stroke_width=3,
                tip_length=0.2
            )

            return current_point, vertical_dash, gradient_arrow, next_x

        # Step 1 시작
        x_value = 2.0  # 시작값
        learning_rate = 0.1

        # 첫 번째 스텝 시각화
        current_point, vertical_dash, gradient_arrow, next_x = create_gradient_descent_visualization(
            self, mid_plane, x_value, learning_rate, 1)

        self.play(Create(vertical_dash), run_time=0.5)
        self.play(FadeIn(current_point))
        self.play(Create(gradient_arrow))

        # Step 1 시작: x₀ = 2
        x_value = 2.0
        learning_rate = 0.1

        # 첫 번째 그래디언트 화살표 생성
        gradient_arrow, next_x = create_gradient_descent_arrow(
            mid_plane, x_value, learning_rate)
        self.play(Create(gradient_arrow))

        # 실제 다음 x 위치 계산
        new_x = calculate_next_x(x_value, learning_rate)
