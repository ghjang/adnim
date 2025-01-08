import sympy as sp
from manim import *
from common.decorator.latex_factory import latex_factory


@latex_factory()
def test_expr() -> str:
    return "f(x) = x^2"


@latex_factory()
def simple_fraction() -> sp.Expr:
    # 문자열 대신 sympy 표현식 반환
    return sp.S(1)/2


@latex_factory()
def sympy_fraction() -> sp.Expr:
    x, y = sp.symbols('x y')
    return (x + y)/(x - y)


@latex_factory()
def sympy_integral() -> sp.Expr:
    x = sp.Symbol('x')
    return sp.Integral(x**2, (x, 0, sp.oo))


@latex_factory()
def sympy_limit() -> sp.Expr:
    x = sp.Symbol('x')
    return sp.Limit(sp.sin(x)/x, x, 0)


@latex_factory()
def sympy_matrix() -> sp.Expr:
    return sp.Matrix([[1, 2], [3, 4]])


class LatexFactoryTest(Scene):
    def construct(self):
        # sympy 표현식을 LaTeX 문자열로 변환 후 MathTex 생성
        equations = VGroup(
            MathTex(test_expr()),
            MathTex(sp.latex(simple_fraction())),
            MathTex(sp.latex(sympy_fraction())),
            MathTex(sp.latex(sympy_integral())),
            MathTex(sp.latex(sympy_limit())),
            MathTex(sp.latex(sympy_matrix()))
        ).arrange(DOWN, buff=0.5)

        # Add all equations to the scene
        self.add(equations)
        self.wait()
