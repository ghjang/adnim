from manim import *
from typing import List, Tuple, Any, Optional
from tex_builder import TexBuilder  # TexBuilder 클래스를 새로운 파일에서 불러옴


class FunctionGraphTest1(Scene):
    def construct(self):
        # 초기 상태 (전체 화면)
        start_plane = NumberPlane(
            x_range=[-8, 8],
            y_range=[-4, 4],
            x_length=16,
            y_length=8,
            background_line_style={
                "stroke_opacity": 0.0  # 처음에는 완전 투명
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

        # 최종 상태 (원하는 위치와 크기)
        end_plane = NumberPlane(
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

        # 원점 점과 그래프는 end_plane 기준으로 생성
        origin_dot = Dot(
            end_plane.c2p(0, 0),
            color=BLUE,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        graph = end_plane.plot(
            lambda x: x**2 - 2,  # y = x² - 2로 변경
            x_range=[-2, 3],
            color=YELLOW
        )

        # 접점 계산 및 생성 (x=2)
        tangent_x = 2
        tangent_y = tangent_x**2 - 2  # y = x² - 2 함수 값으로 수정
        tangent_point = Dot(
            end_plane.c2p(tangent_x, tangent_y),
            color=BLUE_B,  # 색상 변경
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        # 접선 생성 (기울기 = 2x = 4)
        slope = 2 * tangent_x
        # 접선을 그리기 위한 시작점과 끝점 계산
        line_start_x = tangent_x - 1  # 단순히 접선 표시를 위한 x 범위
        line_end_x = tangent_x + 1
        # 접선 방정식: y = f'(x₀)(x - x₀) + f(x₀)
        #            = 4(x - 2) + (4 - 2)
        #            = 4x - 6
        line_start_y = 4 * line_start_x - 6  # 접선의 실제 y값으로 수정
        line_end_y = 4 * line_end_x - 6

        # x축과의 교차점 계산 (다음 이터레이션의 x값)
        # 뉴턴-랩슨 공식: xn+1 = xn - f(xn)/f'(xn)
        next_x = tangent_x - (tangent_x**2 - 2) / \
            (2*tangent_x)  # f(x) = x² - 2 사용
        x_intercept = Dot(
            end_plane.c2p(next_x, 0),
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        # x축 교차점 레이블 추가
        x_label = MathTex(
            f"{float(next_x):.3f}".rstrip('0').rstrip('.'),
            color=GREEN
        )
        x_label.scale(0.8)  # 텍스트 크기 조절
        x_label.next_to(x_intercept, DOWN, buff=0.2)  # 점 아래에 위치

        tangent_line = Line(
            start=end_plane.c2p(line_start_x, line_start_y),
            end=end_plane.c2p(line_end_x, line_end_y),
            color=RED
        )

        # 접점들과 접선을 별도 그룹으로 생성 (점들은 따로)
        tangent_group = VGroup(tangent_line)
        points_group = VGroup(tangent_point, x_intercept, x_label)  # 레이블 추가

        # 첫 번째 이터레이션 (x₀ = 2)
        first_x = 2
        first_y = first_x**2
        first_slope = 2 * first_x
        next_x = first_x - (first_y - 2)/first_slope  # = 1

        # 두 번째 이터레이션 (x₁ = 1.5에서 시작)
        second_x = next_x  # = 1.5
        second_y = second_x**2 - 2  # f(1.5) = 1.5^2 - 2 = 0.25
        second_slope = 2 * second_x  # f'(1.5) = 3
        next_x2 = second_x - second_y/second_slope  # = 1.5 - 0.25/3 ≈ 1.4167

        # 두 번째 접점 (1.5, 0.25)
        second_tangent_point = Dot(
            end_plane.c2p(second_x, second_y),
            color=BLUE_B,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        # 두 번째 접선 (x = 1.5에서 그리기)
        second_line_start_x = second_x - 1
        second_line_end_x = second_x + 1
        # 접선 방정식: y = f'(1.5)(x - 1.5) + f(1.5) = 3(x - 1.5) + 0.25
        second_line_start_y = 3 * (second_line_start_x - second_x) + second_y
        second_line_end_y = 3 * (second_line_end_x - second_x) + second_y

        second_tangent_line = Line(
            start=end_plane.c2p(second_line_start_x, second_line_start_y),
            end=end_plane.c2p(second_line_end_x, second_line_end_y),
            color=RED
        )

        # 두 번째 이터레이션의 x축 교차점
        second_x_intercept = Dot(
            end_plane.c2p(next_x2, 0),  # next_x2 ≈ 1.4167
            color=GREEN,
            radius=DEFAULT_DOT_RADIUS * 0.7
        )

        second_label = MathTex(
            f"{float(next_x2):.3f}".rstrip('0').rstrip('.'),
            color=GREEN
        )
        second_label.scale(0.8)
        second_label.next_to(second_x_intercept, DOWN, buff=0.2)

        second_group = VGroup(second_tangent_line)
        second_points_group = VGroup(
            second_tangent_point, second_x_intercept, second_label)

        # 그룹으로 묶기 (접선 제외)
        start_group = VGroup(start_plane, start_dot, start_graph)
        end_group = VGroup(end_plane, origin_dot, graph)

        # 애니메이션 시퀀스
        self.add(start_group)
        self.wait()
        self.play(
            Transform(start_group, end_group),
            run_time=2
        )
        self.wait()
        # 첫 번째 이터레이션
        self.play(Create(tangent_line), run_time=1)
        self.play(Create(points_group), run_time=0.5)
        self.wait()
        # 두 번째 이터레이션
        self.play(Create(second_group), run_time=1)
        self.play(Create(second_points_group), run_time=0.5)
        self.wait(2)


class FunctionGraphTest2(Scene):
    def setup(self):
        super().setup()
        self.tex_builder = TexBuilder()

    def construct(self):
        tb = self.tex_builder

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
            contents, description_color=GRAY, v_buff=0.5)  # 설명 텍스트 색상을 회색으로 변경
        table.scale(0.8)
        table.next_to(title, DOWN, buff=0.5)

        self.play(Create(table), run_time=0.5 * len(contents))
        self.wait(2)

        # 마지막 수식을 테이블에서 복제하여 화면 좌상단으로 이동
        last_equation = table.get_entries(pos=(5, 1))[-1].copy()
        self.play(
            last_equation.animate.to_edge(UP + LEFT),
            FadeOut(title),
            FadeOut(table)
        )
        self.wait(2)


class ColoredMathExample(Scene):
    def setup(self):
        super().setup()
        self.tex_builder = TexBuilder()

    def construct(self):
        eq_parts = [
            r"f'(x)",
            "=",
            (r"2x", RED)
        ]

        # Builder 객체를 통해 MathTex 생��
        derivative = self.tex_builder.create_colored_tex(eq_parts)
        self.play(Write(derivative))
        self.wait(2)


class EquationWithDescription(Scene):
    def setup(self):
        super().setup()
        self.tex_builder = TexBuilder()

    def construct(self):
        contents = [
            (r"x^2 = 2", "Given equation"),
            (["f(x)", "=", ("x^2 - 2", YELLOW)], "Convert to function form"),
            ([(r"f'(x) = 2x", RED)], "Derivative of function"),
            (r"x = \sqrt{2}", None),  # 설명이 없는 경우
            (r"x = \sqrt[12]{2}", None)  # 설명이 없는 경우
        ]

        table = self.tex_builder.create_equation_table(contents)
        table.scale(0.8)
        table.center()

        self.play(Create(table))
        self.wait(2)


class ColoredFractionExample(Scene):
    def construct(self):
        # 분자와 분모에 다른 색상을 적용한 분수 예제
        fraction = MathTex(
            r"{x_n^2 - 2}", r"\over", r"{2x_n}"
        )

        self.play(Write(fraction))
        self.wait(2)


class ShowScreenResolution(Scene):
    def construct(self):
        pixel_height = config["pixel_height"]  # 1080 is default
        pixel_width = config["pixel_width"]  # 1920 is default
        frame_width = config["frame_width"]
        frame_height = config["frame_height"]
        self.add(Dot())
        d1 = Line(frame_width * LEFT / 2,
                  frame_width * RIGHT / 2).to_edge(DOWN)
        self.add(d1)
        self.add(Text(str(frame_width)).next_to(d1, UP))
        self.add(Text(str(pixel_width)).next_to(d1, UP * 4))
        d2 = Line(frame_height * UP / 2, frame_height * DOWN / 2).to_edge(LEFT)
        self.add(d2)
        self.add(Text(str(frame_height)).next_to(d2, RIGHT))
        self.add(Text(str(pixel_height)).next_to(d2, RIGHT * 5))
