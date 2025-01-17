import sympy as sp
from manim import *
from common.decorator.latex_factory import latex_factory


@latex_factory()
def diff_expr() -> sp.Expr:
    x = sp.Symbol('x')
    eq = (x + 1)**2 - x**2 + sp.sin(x)
    expand = sp.expand(eq)
    return sp.diff(expand, x)


@latex_factory()
def test_list_assignment() -> str:
    x = 100
    values = [
        x,
        x + 1,
        x + 2
    ]
    return "x = 42"


@latex_factory()
def test_list_assignment_1() -> str:
    x = 100
    values = [x, x + 1, x + 2]
    return "x = 42"


@latex_factory()
def test_list_assignment_2() -> str:
    x = 100
    values = [x,
              x + 1, x + 2]
    return "x = 42"


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
def sympy_limit(
        dummy: int = 0
) -> sp.Expr:
    x = sp.Symbol('x')
    return sp.Limit(sp.sin(x)/x, x, 0)


@latex_factory()
def sympy_matrix() -> sp.Expr:
    return sp.Matrix([[1, 2], [3, 4]])


@latex_factory(auto_latex_str=False)
def test_expr_original() -> sp.Expr:
    y = sp.Symbol('y')
    return sp.Limit(sp.sin(y)/y, y, 0)


# @latex_factory()
def test_expr_auto() -> str:
    return "f(x) = x^2"


@latex_factory()
def test_args(x: int, y: int) -> int:
    return x + y


class LatexFactoryTest(Scene):
    @latex_factory()
    def instance_method_test(self) -> str:
        x = sp.Symbol('x')
        return "f'(x) = 2x"

    def construct(self):
        diff_expr()
        test_expr()
        test_list_assignment()
        test_list_assignment_1()
        test_list_assignment_2()
        test_args(1, 2)

        self.instance_method_test()

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
