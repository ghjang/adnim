import sympy as sp
from manim import *
from common.decorator.latex_factory import latex_factory


@latex_factory()
def test_expr() -> str:
    return "f(x) = x^2"


# @latex_factory()
def simple_fraction() -> sp.Expr:
    # 문자열 대신 sympy 표현식 반환
    return sp.S(1)/2


# @latex_factory()
def sympy_fraction() -> sp.Expr:
    x, y = sp.symbols('x y')
    return (x + y)/(x - y)


# @latex_factory()
def sympy_integral() -> sp.Expr:
    x = sp.Symbol('x')
    return sp.Integral(x**2, (x, 0, sp.oo))


# @latex_factory()
def sympy_limit() -> sp.Expr:
    x = sp.Symbol('x')
    return sp.Limit(sp.sin(x)/x, x, 0)


# @latex_factory()
def sympy_matrix() -> sp.Expr:
    return sp.Matrix([[1, 2], [3, 4]])


# @latex_factory(auto_latex_str=False)
def test_expr_original() -> sp.Expr:
    y = sp.Symbol('y')
    return sp.Limit(sp.sin(y)/y, y, 0)


# @latex_factory()
def test_expr_auto() -> str:
    return "f(x) = x^2"


class LatexFactoryTest(Scene):
    def construct(self):
        test_expr()
        
        original = MathTex(sp.latex(test_expr_original()))

        auto = MathTex(test_expr_auto())

        # 나머지 예제들
        equations = VGroup(
            original,
            auto,
            MathTex(simple_fraction()),
            MathTex(sympy_fraction()),
            MathTex(sympy_integral()),
            MathTex(sympy_limit()),
            MathTex(sympy_matrix())
        ).arrange_in_grid(3, 3, buff=1)

        self.add(equations)
        self.wait()
