from manim import *
from sympy import *
from sympy.abc import x, y
from sympy.printing.latex import LatexPrinter


def custom_latex(expr):
    latex_printer = LatexPrinter({'mul_symbol': 'dot'})
    return latex_printer.doprint(expr)


class SymPyDemoScene(Scene):
    def construct(self):
        # 모두 다른 꼴을 의도한 예시 수식
        expr = (x + y)*(x + 2) + y**3

        # 차수 정렬(내림차순) 함수 (상수항은 마지막)
        def custom_order(exp_expr, var):
            terms = exp_expr.collect(var, evaluate=False)

            def sort_key(k):
                # 해당 변수의 차수 확인, 0이면 맨 뒤로
                deg = degree(k, var)
                return -999 if deg == 0 else deg
            powers = sorted(terms.keys(), key=sort_key, reverse=True)
            return sum(terms[p]*p for p in powers)

        # 전개
        expanded = expand(expr)
        expand_tex = MathTex(r"\text{Expanded: }", custom_latex(expanded))

        # x에 대한 collect
        collected_x = custom_order(expanded, x)
        collect_x_tex = MathTex(r"\text{Collected in }x\text{: }",
                                custom_latex(collected_x))

        # y에 대한 collect
        collected_y = custom_order(expanded, y)
        collect_y_tex = MathTex(r"\text{Collected in }y\text{: }",
                                custom_latex(collected_y))

        # 간단히 화면에 배치
        title = Text("SymPy Demo", color=BLUE).to_edge(UP)
        self.play(FadeIn(title))

        original = MathTex(r"\text{Original: }", custom_latex(expr))
        original.next_to(title, DOWN, buff=1)
        self.play(FadeIn(original))

        expand_tex.next_to(original, DOWN, buff=0.3)
        self.play(FadeIn(expand_tex))

        collect_x_tex.next_to(expand_tex, DOWN, buff=0.3)
        self.play(FadeIn(collect_x_tex))

        collect_y_tex.next_to(collect_x_tex, DOWN, buff=0.3)
        self.play(FadeIn(collect_y_tex))

        # y에 대해서 미분
        d_collected_y = diff(collected_y, y)
        d_collected_y_tex = MathTex(
            r"\frac{\partial}{\partial y}\bigl(\text{collect in }y\bigr)\,=\,",
            custom_latex(d_collected_y)
        )
        d_collected_y_tex.next_to(collect_y_tex, DOWN, buff=0.3)
        self.play(FadeIn(d_collected_y_tex))

        self.wait(2)
