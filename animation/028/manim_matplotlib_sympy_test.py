from manim import *
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import sympy as sp
from sympy.utilities.lambdify import lambdify


class Display3DPlot(Scene):
    def construct(self):
        # sympy를 사용해 함수 정의
        x, y = sp.symbols("x y")
        r2 = x**2 + y**2
        func_expr = r2**2 - 4 * r2 + 2 * x + 3 * y + 2

        # sympy에서 LaTeX 문자열 생성
        func_latex = sp.latex(func_expr)

        # 좌측 영역에 모든 수식 배치
        left_group = VGroup()

        # 함수 표현식 표시 - 폰트 크기 줄임
        formula = MathTex(r"f(x, y) = " + func_latex, font_size=28)
        formula.to_edge(UP).to_edge(LEFT, buff=0.5)
        left_group.add(formula)

        # 다양한 수식 형태 표시
        expanded_expr = sp.expand(func_expr)
        simplified_expr = sp.simplify(func_expr)
        collected_expr = sp.collect(expanded_expr, r2)

        expanded_tex = MathTex(
            r"\text{Expanded: } f(x, y) = " + sp.latex(expanded_expr), font_size=24
        )
        simplified_tex = MathTex(
            r"\text{Simplified: } f(x, y) = " + sp.latex(simplified_expr), font_size=24
        )
        collected_tex = MathTex(
            r"\text{Collected: } f(x, y) = " + sp.latex(collected_expr), font_size=24
        )

        # 왼쪽 정렬로 수식 배치
        expanded_tex.next_to(formula, DOWN, buff=0.3).align_to(formula, LEFT)
        simplified_tex.next_to(expanded_tex, DOWN, buff=0.3).align_to(
            expanded_tex, LEFT
        )
        collected_tex.next_to(simplified_tex, DOWN, buff=0.3).align_to(
            simplified_tex, LEFT
        )

        left_group.add(expanded_tex, simplified_tex, collected_tex)

        # 미분 계산하여 표시
        df_dx = sp.diff(func_expr, x)
        df_dy = sp.diff(func_expr, y)

        # 미분 결과 간소화
        df_dx_simplified = sp.simplify(df_dx)
        df_dy_simplified = sp.simplify(df_dy)

        derivative_text = Text("Partial Derivatives:", font_size=24)
        derivative_text.next_to(collected_tex, DOWN, buff=0.4).align_to(
            collected_tex, LEFT
        )
        left_group.add(derivative_text)

        df_dx_tex = MathTex(
            r"\frac{\partial f}{\partial x} = " + sp.latex(df_dx_simplified),
            font_size=22,
        )
        df_dx_tex.next_to(derivative_text, DOWN, buff=0.2).align_to(
            derivative_text, LEFT
        )
        left_group.add(df_dx_tex)

        df_dy_tex = MathTex(
            r"\frac{\partial f}{\partial y} = " + sp.latex(df_dy_simplified),
            font_size=22,
        )
        df_dy_tex.next_to(df_dx_tex, DOWN, buff=0.2).align_to(df_dx_tex, LEFT)
        left_group.add(df_dy_tex)

        # 임계점 찾기
        critical_points_text = Text("Critical Points:", font_size=24)
        critical_points_text.next_to(df_dy_tex, DOWN, buff=0.4).align_to(
            derivative_text, LEFT
        )
        left_group.add(critical_points_text)

        critical_point_formula = MathTex(
            r"\text{Where } \frac{\partial f}{\partial x} = 0 \text{ and } \frac{\partial f}{\partial y} = 0",
            font_size=22,
        )
        critical_point_formula.next_to(critical_points_text, DOWN, buff=0.2).align_to(
            critical_points_text, LEFT
        )
        left_group.add(critical_point_formula)

        # 전체 왼쪽 그룹을 좀 더 왼쪽으로 조정
        left_group.to_edge(LEFT, buff=0.5)

        # 오른쪽에 3D 플롯 이미지 배치
        # sympy 함수를 사용해 3D 플롯 생성
        plot_image = self.create_3d_plot(func_expr, x, y)
        plot_image.scale(0.5)  # 크기 조정

        # 오른쪽 중앙에 배치
        plot_image.to_edge(RIGHT, buff=0.5).scale(0.6)

        # 애니메이션 시퀀스
        # 1. 수식 먼저 표시
        self.play(FadeIn(formula))
        self.play(FadeIn(expanded_tex))
        self.play(FadeIn(simplified_tex))
        self.play(FadeIn(collected_tex))

        # 2. 3D 플롯 이미지 페이드인
        self.play(FadeIn(plot_image))

        # 3. 나머지 미분 수식 표시
        self.play(FadeIn(derivative_text))
        self.play(FadeIn(df_dx_tex), FadeIn(df_dy_tex))
        self.play(FadeIn(critical_points_text), FadeIn(critical_point_formula))

        # final wait
        self.wait(2)

    def create_3d_plot(self, func_expr, x_sym, y_sym):
        # sympy 표현식을 numpy에서 사용 가능한 함수로 변환
        f_numpy = lambdify((x_sym, y_sym), func_expr, "numpy")

        # 3D 그래프 그리기 위한 x, y 좌표 설정
        x = np.linspace(-2, 2, 100)
        y = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x, y)
        Z = f_numpy(X, Y)  # 각 좌표에 대한 sympy 함수 값 계산

        # 3D 그래프 플로팅
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")

        surface = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="k", alpha=0.8)

        # 축 설정
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        ax.set_title("3D Function Graph with SymPy")

        # 컬러바 추가
        fig.colorbar(surface, ax=ax, shrink=0.5, aspect=5)

        # 메모리에 이미지로 저장
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)

        # manim의 ImageMobject로 변환
        return ImageMobject(Image.open(buf)).set_resampling_algorithm(
            RESAMPLING_ALGORITHMS["lanczos"]
        )
