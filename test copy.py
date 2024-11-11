from manim import *
from typing import List, Tuple, Any, Optional


class TexBuilder:
    """Tex 객체 생성을 위한 유틸리티 클래스

    수식과 색상 정보를 튜플 리스트로 받아 색상이 적용된 Tex 객체를 생성합니다.
    """

    def extract_items(self, parts: List[Tuple], idx: int) -> List:
        """튜플 리스트에서 특정 인덱스의 아이템만 추출

        Args:
            parts: 추출할 데이터가 있는 튜플 리스트
            idx: 추출할 튜플의 인덱스

        Returns:
            List: 추출된 아이템들의 리스트
        """
        return [part[idx] for part in parts]

    def create_colored_tex(
        self,
        eq_parts: List[Tuple[str, Any]],
        position: Optional[Tuple] = None,
        default_color: Any = WHITE,
        **kwargs
    ) -> MathTex:
        """색상이 적용된 MathTex 객체 생성

        Args:
            eq_parts: [(수식, 색상), ...] 또는 [수식, ...] 형태의 리스트
            position: (참조객체, 방향, 간격) 형태의 위치 정보 튜플
            default_color: 기본 텍스트 색상
            **kwargs: MathTex 생성시 추가 인자

        Returns:
            MathTex: 색상이 적용된 수식 객체

        Example:
            >>> eq_parts = [(r"f'(x)", BLUE), ("=", WHITE), ("2x", RED)]
            >>> tex = builder.create_colored_tex(eq_parts)
        """
        # 문자열만 지정된 경우 기본 색상으로 처리
        eq_parts = [(part, default_color) if isinstance(
            part, str) else part for part in eq_parts]
        formulas = self.extract_items(eq_parts, 0)

        tex = MathTex(
            *formulas,
            substrings_to_isolate=formulas,
            **kwargs
        )

        for i, (_, color) in enumerate(eq_parts):
            tex[i].set_color(color)

        if position:
            ref_obj, direction, buff = position
            tex.next_to(ref_obj, direction, buff=buff)

        return tex

    def create_equation_table(
        self,
        contents: List[Tuple[Any, Optional[str]]],
        default_color: Any = WHITE,
        **kwargs
    ) -> VGroup:
        """수식과 설명을 포함한 테이블 생성

        Args:
            contents: [(수식 또는 [(수식, 색상)], 설명), ...] 형태의 리스트
            default_color: 기본 텍스트 색상
            **kwargs: VGroup 생성시 추가 인자

        Returns:
            VGroup: 수식과 설명이 포함된 테이블 객체
        """
        equations = []
        descriptions = []

        for eq_parts, desc in contents:
            # 문자열만 지정된 경우 기본 색상으로 처리
            if isinstance(eq_parts, str):
                eq_parts = [(eq_parts, default_color)]
            else:
                eq_parts = [(part, default_color) if isinstance(
                    part, str) else part for part in eq_parts]
            equation = self.create_colored_tex(eq_parts)
            if desc:
                equations.append(equation)
                description = Text("; " + desc, font_size=24)
                description.next_to(equation, RIGHT, buff=0.2)
                descriptions.append(description)
            else:
                if equations:
                    last_eq = equations[-1]
                    if isinstance(last_eq, VGroup):
                        last_eq.add(equation)
                    else:
                        new_group = VGroup(last_eq, equation).arrange(DOWN, buff=0.4)
                        equations[-1] = new_group
                else:
                    equations.append(equation)

        rows = VGroup()
        for eq, desc in zip(equations, descriptions):
            row = VGroup(eq, desc).arrange(RIGHT, buff=2.0)
            rows.add(row)

        rows.arrange(DOWN, buff=0.8)
        return rows

    def create_multiline_tex(
        self,
        eq_lines: List[List[Tuple[str, Any]]],
        default_color: Any = WHITE,
        **kwargs
    ) -> VGroup:
        """여러 수식을 행으로 배치한 Tex 객체 생성

        Args:
            eq_lines: [[(수식, 색상), ...], ...] 형태의 리스트
            default_color: 기본 텍스트 색상
            **kwargs: VGroup 생성시 추가 인자

        Returns:
            VGroup: 여러 수식이 행으로 배치된 객체
        """
        lines = VGroup()
        for eq_parts in eq_lines:
            eq_parts = [(part, default_color) if isinstance(part, str) else part for part in eq_parts]
            line = self.create_colored_tex(eq_parts)
            lines.add(line)
        lines.arrange(DOWN, **kwargs)
        return lines


class FunctionGraphTest1(Scene):
    def construct(self):
        # 초기 상태 (��체 화면)
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
            (r"\text{Newton-Raphson Method: Finding }", WHITE),
            (r"\sqrt{2}", GREEN)
        ]
        title = tb.create_colored_tex(title_parts)
        title.to_edge(UP)
        self.play(FadeIn(title))

        equation_parts = [(r"x^2 = 2", WHITE)]
        equation = tb.create_colored_tex(equation_parts)
        equation.next_to(title, DOWN, buff=0.5)
        self.play(Write(equation))

        equation2_parts = [(r"f(x) = x^2 - 2", WHITE)]
        equation2 = tb.create_colored_tex(equation2_parts)
        equation2.next_to(equation, DOWN, buff=0.5)
        self.play(Write(equation2))

        derivative_parts = [(r"f'(x) = 2x", WHITE)]
        derivative = tb.create_colored_tex(derivative_parts)
        derivative.next_to(equation2, DOWN, buff=0.5)
        self.play(Write(derivative))

        newton_raphson_formula_parts = [
            (r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}", WHITE)
        ]
        newton_raphson_formula = tb.create_colored_tex(
            newton_raphson_formula_parts)
        newton_raphson_formula.next_to(derivative, DOWN, buff=0.5)
        self.play(Write(newton_raphson_formula))

        formular_eq_parts = [
            (r"x_{n+1} = x_n - \frac{x_n^2 - 2}{2x_n}", WHITE)
        ]
        formular_eq = tb.create_colored_tex(formular_eq_parts)
        formular_eq.next_to(newton_raphson_formula, DOWN, buff=0.5)
        self.play(Write(formular_eq))

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

        # Builder 객체를 통해 MathTex 생성
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
            (r"x = \sqrt{2}", None)  # 설명이 없는 경우
        ]

        table = self.tex_builder.create_equation_table(contents)
        table.scale(0.8)
        table.to_edge(UP)

        self.play(Create(table))
        self.wait(1)

        # 여러 수식을 행으로 배치한 예제
        multiline_eq = [
            [(r"x^2", WHITE), ("=", WHITE), (r"2", YELLOW)],
            [(r"f(x)", WHITE), ("=", WHITE), (r"x^2 - 2", YELLOW)],
            [(r"f'(x)", WHITE), ("=", WHITE), (r"2x", RED)]
        ]

        multiline_tex = self.tex_builder.create_multiline_tex(multiline_eq)
        multiline_tex.to_edge(DOWN)
        self.play(Create(multiline_tex))
        self.wait(2)
