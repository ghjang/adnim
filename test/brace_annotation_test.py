from manim import *


class BraceAnnotation(Scene):
    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        b2 = Brace(
            line,
            direction=line.copy().rotate(PI / 2).get_unit_vector()
        )
        lineCopy = line.copy().rotate(PI / 2).set_color(RED)
        b2text = b2.get_tex("x-x_1")
        # b2text = b2.get_tex(f"lineCopy: {lineCopy.get_unit_vector()}, {lineCopy.get_angle()}, {lineCopy.get_start()}, {lineCopy.get_end()}")
        # b2text = b2.get_tex(f"lineCopy: {lineCopy.get_unit_vector()}, {lineCopy.get_start()}, {lineCopy.get_end()}").shift(RIGHT * 4)
        self.add(line, dot, dot2, b1, b2, b1text, b2text)
        self.add(lineCopy)
        arrow = Arrow(ORIGIN, lineCopy.get_unit_vector(), color=GREEN)
        self.add(arrow)

        b3 = Brace(line, direction=RIGHT)
        b3text = b3.get_text("RIGHT")
        self.add(b3, b3text)

        b4 = Brace(line, direction=UP)
        b4text = b4.get_text("UP")
        self.add(b4, b4text)

        b5 = Brace(line, direction=DOWN)
        b5text = b5.get_text("DOWN")
        # self.add(b5, b5text)

        b6 = Brace(line, direction=LEFT)
        b6text = b6.get_text("LEFT")
        self.add(b6, b6text)
