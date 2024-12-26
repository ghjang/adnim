from manim import *
import numpy as np


class WrappingUnitCircleWithNumberLine(Scene):
    def construct(self):
        # Create circle
        circle = Circle(radius=2, color=WHITE)

        # Create number line
        number_line = NumberLine(
            x_range=[-PI, PI, PI/4],
            length=4*PI,
            color=YELLOW,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 1}
        )

        # Position number line above circle
        number_line.shift(UP * 3)

        # Create the path for wrapping animation
        path = ParametricFunction(
            lambda t: np.array([
                2 * np.cos(t),
                2 * np.sin(t),
                0
            ]),
            t_range=[0, 2*PI],
            color=YELLOW
        )

        # Animation sequence
        self.play(Create(circle))
        self.play(Create(number_line))
        self.wait()

        # Transform number line into circular path
        self.play(
            Transform(number_line, path),
            run_time=3
        )

        self.wait(2)


class WrappingUnitCircleWithNumberLine1(Scene):
    def construct(self):
        self.play(Create(Circle(radius=2, color=ORANGE)))
        self.wait(2)
