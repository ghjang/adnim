from manim import *


class RightAngleTest(Scene):
    def construct(self):
        line1 = Line(ORIGIN, RIGHT)
        line2 = Line(ORIGIN, UP)
        mob = RightAngle(line1, line2, color=YELLOW, stroke_width=7)
        self.add(VGroup(mob, line1, line2).shift(DL*0.3))


class AngleTest(Scene):
    def construct(self):
        line1 = Line(LEFT*0.2, RIGHT)
        line2 = Line(DOWN*0.2, UP)
        a = Angle(line1, line2, dot=True, color=YELLOW, dot_color=YELLOW)
        self.add(VGroup(line1, line2, a).move_to(ORIGIN))


class AngleWithLabelTest(Scene):
    def construct(self):
        line1 = Line((LEFT+(1/3)*UP)*0.1, RIGHT+(1/3)*DOWN)
        line2 = Line((DOWN+(1/3)*RIGHT)*0.1, UP+(1/3)*LEFT)
        angle = Angle(line1, line2, radius=0.3)
        value = Integer(angle.get_value(degrees=True),
                        unit='^{\circ}', color=YELLOW)
        value.next_to(angle, UR, buff=0)
        self.add(VGroup(line1, line2, angle, value).move_to(ORIGIN))
