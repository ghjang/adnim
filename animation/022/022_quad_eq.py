from manim import *


class QuadraticFormulaDerivation(Scene):
    def construct(self):
        latexes = [
            MathTex("F'(x) = f(x)"),
        ]

        latexes.append(MathTex("ax^2 + bx + c = 0"))
        latexes.append(MathTex("x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}"))

        latexes.append(MathTex("E = mc^2"))

        for tex in latexes:
            self.play(Write(tex))
            self.wait()
        self.wait()

    def test(self):
        tex = MathTex("ax^2 + bx + c = 0")
        pass
