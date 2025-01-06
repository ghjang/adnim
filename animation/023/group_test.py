from manim import *

class VGroupTest(Scene):
    def construct(self):
        g = VGroup(
            Square(color=GREEN),
            Circle(),
            Text("Hello", color=GREEN)
        )

        self.add(g)
        self.wait(2)
        
        self.play(
            g.animate.shift(UP).set_opacity(0.25),
            run_time=2
        )

        self.wait(2)