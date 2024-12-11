from manim import *


class ThreeDAxesExample(ThreeDScene):
    def construct(self):
        number_plane = NumberPlane()
        self.add(number_plane)

        axes = ThreeDAxes()
        x_label = axes.get_x_axis_label(Text("x", font_size=60, color=TEAL))
        y_label = axes.get_y_axis_label(Text("y", font_size=60, color=TEAL))
        z_label = axes.get_z_axis_label(Text("z", font_size=60, color=TEAL))
        axis_labels = VGroup(x_label, y_label, z_label)
        self.add(axes, axis_labels)

        text = Text("3D Axes Example", font_size=68, color=RED)
        self.add(text)
