from manim import *


class UnitVector(Scene):
    def construct(self):
        a1 = Vector([1, 0, 0], color=BLUE)
        b1 = Vector([0, 1, 0], color=GREEN)
        self.add(a1, b1)

        origin_dot = Dot(ORIGIN, color=RED)
        self.add(origin_dot)

        a2 = Vector(RIGHT * 2, color=BLUE).shift(DOWN / 2 )
        b2 = Vector(UP * 2, color=GREEN).shift(LEFT / 2)
        self.add(a2, b2)
