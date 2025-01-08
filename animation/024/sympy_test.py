from manim import *
import sympy as sp
from sympy.printing.latex import LatexPrinter


def custom_latex(expr):
    latex_printer = LatexPrinter({'mul_symbol': 'dot'})
    return latex_printer.doprint(expr)


class MathFunction(Scene):
    # 화면 구성 설정
    CONFIG = {
        "text_font_size": 48,
        "formula_font_size": 72,
        "plot_formula_font_size": 40,
        "grid_buff": 0.7,
    }

    # 플롯 설정 추가
    PLOT_CONFIG = {
        "x_range": [-5, 5, 1],
        "y_range": [-4, 6, 1],
        "background_opacity": 0.6,
        "formula_position": {
            "x": 3,
            "y": 4.5,
        },
        "plot_margins": {
            "y_min_factor": 0.2,  # y축 하단 여유 공간 비율
            "y_max_factor": 0.8,  # y축 상단 여유 공간 비율
            "x_margin_factor": 0.1,  # x축 좌우 여유 공간 비율
        },
        # 샘플링 포인트 수를 해상도 기반으로 계산
        "sampling_points": max(
            200,  # 최소 기본값 (낮은 해상도용)
            min(   # 최대값 제한
                int(config.pixel_width / 2),  # 해상도의 1/2
                2000  # 최대 상한값
            )
        )
    }

    # 색상 설정
    COLORS = {
        "text": YELLOW_A,
        "original": BLUE_B,
        "first_derivative": GREEN_B,
        "second_derivative": RED_B,
    }

    # 텍스트 설정
    LABELS = {
        "original": "Original Function:",
        "first": "First Derivative:",
        "second": "Second Derivative:",
    }

    def create_plot(self, func, color, latex_expr):
        """그래프 플롯 생성 헬퍼 메서드"""
        def find_valid_range(func, x_range, y_range):
            x_min, x_max = x_range[0], x_range[1]
            y_min, y_max = y_range[0], y_range[1]
            
            # y축 범위 설정
            y_unit = y_range[2] if len(y_range) > 2 else 1
            y_safe_min = y_min + y_unit * self.PLOT_CONFIG["plot_margins"]["y_min_factor"]
            y_safe_max = y_max - y_unit * self.PLOT_CONFIG["plot_margins"]["y_max_factor"]
            
            # 샘플링
            x_test = np.linspace(x_min, x_max, self.PLOT_CONFIG["sampling_points"])
            y_test = func(x_test)
            
            # 범위 체크
            valid_indices = (y_test >= y_safe_min) & (y_test <= y_safe_max)
            valid_x = x_test[valid_indices]
            
            if len(valid_x) == 0:
                return [x_min, x_min]
            
            # x축 여유 공간
            x_unit = x_range[2] if len(x_range) > 2 else 1
            x_margin = x_unit * self.PLOT_CONFIG["plot_margins"]["x_margin_factor"]
            
            return [
                max(x_min, valid_x[0] - x_margin),
                min(x_max, valid_x[-1] + x_margin)
            ]

        # 넘버플레인 생성
        plane = NumberPlane(
            x_range=self.PLOT_CONFIG["x_range"],
            y_range=self.PLOT_CONFIG["y_range"],
            background_line_style={
                "stroke_opacity": self.PLOT_CONFIG["background_opacity"]
            }
        ).add_coordinates()

        # 유효한 x 범위 찾기 (NumberPlane의 설정값 사용)
        plot_range = find_valid_range(
            func,
            self.PLOT_CONFIG["x_range"],  # x축 전체 범위
            self.PLOT_CONFIG["y_range"]   # NumberPlane의 y축 범위
        )

        # 찾은 범위에서 그래프 생성
        graph = plane.plot(
            func,
            x_range=plot_range,
            use_smoothing=True,
            color=color
        )

        # 수식 생성
        formula = MathTex(
            latex_expr,
            color=color,
            font_size=self.CONFIG["plot_formula_font_size"]
        )

        # 수식 위치 조정
        formula.move_to(
            plane.coords_to_point(
                self.PLOT_CONFIG["formula_position"]["x"],
                self.PLOT_CONFIG["formula_position"]["y"]
            )
        )

        # 모든 요소를 하나의 VGroup으로 묶기
        plot_group = VGroup()
        plot_group.add(plane)
        plot_group.add(graph)
        plot_group.add(formula)

        return plot_group

    def construct(self):
        self.next_section(
            "Math Function Example: f(x) = x * exp(x)", skip_animations=True)

        # 변수와 함수 정의
        x = sp.Symbol('x')
        f = x * sp.exp(x)
        f_prime = sp.factor(sp.diff(f, x))
        f_double_prime = sp.factor(sp.diff(f_prime, x))

        # 설명 텍스트 생성
        texts = VGroup(
            Text(self.LABELS["original"], font_size=self.CONFIG["text_font_size"],
                 color=self.COLORS["text"]),
            Text(self.LABELS["first"], font_size=self.CONFIG["text_font_size"],
                 color=self.COLORS["text"]),
            Text(self.LABELS["second"], font_size=self.CONFIG["text_font_size"],
                 color=self.COLORS["text"])
        )

        # 수식 생성
        formulas = VGroup(
            MathTex(f"f(x) = {custom_latex(f)}",
                    font_size=self.CONFIG["formula_font_size"],
                    color=self.COLORS["original"]),
            MathTex(f"f'(x) = {custom_latex(f_prime)}",
                    font_size=self.CONFIG["formula_font_size"],
                    color=self.COLORS["first_derivative"]),
            MathTex(f"f''(x) = {custom_latex(f_double_prime)}",
                    font_size=self.CONFIG["formula_font_size"],
                    color=self.COLORS["second_derivative"])
        )

        # 모든 요소를 하나의 VGroup으로 결합
        all_elements = VGroup()
        for text, formula in zip(texts, formulas):
            all_elements.add(text, formula)

        # 3x2 그리드로 배치
        all_elements.arrange_in_grid(
            rows=3,
            cols=2,
            col_alignments=['r', 'l'],
            buff=self.CONFIG["grid_buff"]
        )

        # 애니메이션
        self.add(all_elements)
        self.wait(1)

        self.next_section("Plot Original Function", skip_animations=True)

        # 이전 내용 페이드아웃
        self.play(FadeOut(all_elements))

        # sympy 함수를 파이썬 람다로 변환
        f_lambda = sp.lambdify(x, f, modules=['numpy'])

        # 원본 함수 플롯 생성 및 표시
        original_plot = self.create_plot(
            lambda x: f_lambda(x),
            self.COLORS["original"],
            f"f(x) = {custom_latex(f)}"
        )

        self.play(FadeIn(original_plot))
        self.wait(2)

        self.next_section("Plot First Derivative", skip_animations=True)

        # 이전 플롯 제거
        self.play(FadeOut(original_plot))

        # 1계 도함수의 람다 함수 생성
        f_prime_lambda = sp.lambdify(x, f_prime, modules=['numpy'])

        # 1계 도함수 플롯 생성 및 표시
        derivative_plot = self.create_plot(
            lambda x: f_prime_lambda(x),
            self.COLORS["first_derivative"],
            f"f'(x) = {custom_latex(f_prime)}"
        )

        self.play(FadeIn(derivative_plot))
        self.wait(2)

        # 다음 섹션 준비
        self.next_section("Plot Second Derivative", skip_animations=True)
        self.play(FadeOut(derivative_plot))

        # 2계 도함수의 람다 함수 생성
        f_double_prime_lambda = sp.lambdify(
            x, f_double_prime, modules=['numpy'])

        # 2계 도함수 플롯 생성 및 표시
        second_derivative_plot = self.create_plot(
            lambda x: f_double_prime_lambda(x),
            self.COLORS["second_derivative"],
            f"f''(x) = {custom_latex(f_double_prime)}"
        )

        self.play(FadeIn(second_derivative_plot))
        self.wait(2)

        self.next_section("Show All Plots in Grid")

        # 이전 플롯 제거
        self.play(FadeOut(second_derivative_plot))

        # 각 플롯을 복제하여 새로운 인스턴스 생성
        plots = VGroup(
            original_plot.copy(),
            derivative_plot.copy(),
            second_derivative_plot.copy()
        ).arrange_in_grid(
            rows=1,
            cols=3,
            buff=0.5
        )

        # 전체 그룹의 크기 조정
        plots.scale(0.4)
        plots.move_to(ORIGIN)

        # 애니메이션
        self.play(FadeIn(plots))
        self.wait(2)

        # 마지막 섹션 종료
        self.next_section("End")
        self.play(FadeOut(plots))
