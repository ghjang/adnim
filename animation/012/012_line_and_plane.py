from manim import *

config.frame_rate = 10


class Conditions(ThreeDScene):
    def construct(self):
        self.next_section(
            "1. Intro of Conditions for determining a line",
            skip_animations=False
        )

        # Title with gradient color
        title = Text("Conditions for Determining a Line", font_size=60)
        title.set_color_by_gradient(PURPLE_E, GREEN_E, PINK, YELLOW_E)
        self.play(FadeIn(title))
        self.wait()
        self.play(
            title.animate.to_edge(UP, buff=0.1).set_opacity(0),
            run_time=1
        )

        self.next_section(
            "2. Show Conditions for determining a line in 2D",
            skip_animations=False
        )

        # 2D plane with customized axis colors
        plane = NumberPlane(
            x_range=[-4, 4],
            y_range=[-3, 3],
            background_line_style={
                "stroke_opacity": 0.4,
                "stroke_color": TEAL_B
            },
            x_axis_config={"color": PURPLE},
            y_axis_config={"color": PURPLE}
        ).to_edge(DOWN)
        self.play(FadeIn(plane))

        # Two points
        point1 = Dot(point=plane.coords_to_point(-2, -1),
                     color=GREEN).set_z_index(2)
        point2 = Dot(point=plane.coords_to_point(
            2, 1), color=GREEN).set_z_index(2)
        points_label = Text(
            "Line is determined by Two Points",
            t2c={
                "Line": YELLOW_C,
                "is determined by": LIGHT_GREY,
                "Two Points": GREEN
            }
        ).to_edge(UP, buff=0.35)

        self.play(FadeIn(points_label))
        self.wait(0.75)
        self.play(Create(point1), Create(point2))

        # Line
        line = Line(
            point1.get_center(),
            point2.get_center(),
            color=YELLOW_C
        ).set_z_index(1)
        self.play(Create(line))
        self.wait()

        self.next_section(
            "3. Show Conditions for determining a line in 3D",
            skip_animations=True
        )

        # 3D transition preparation
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        # 3D axes with customized colors
        axes = ThreeDAxes(
            axis_config={"color": TEAL_B}
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # 3D points
        point3d1 = Dot3D(point=axes.coords_to_point(-2, -1, 1), color=GREEN)
        point3d2 = Dot3D(point=axes.coords_to_point(2, 1, -1), color=GREEN)

        # 3D line
        line3d = Line3D(
            start=point3d1.get_center(),
            end=point3d2.get_center(),
            color=YELLOW_C
        )

        # 3D title with adjusted color mapping to avoid ambiguity
        line_text = Text("Line", color=YELLOW_C)
        in_text = Text(" in ", color=LIGHT_GREY)
        space_text = Text("Space", color=PURPLE)
        title3d = VGroup(
            line_text,
            in_text,
            space_text
        ).arrange().to_edge(UP)

        self.add(axes, title3d)
        self.play(
            Create(point3d1),
            Create(point3d2)
        )
        self.wait()
        self.play(Create(line3d))
        self.wait()

        # 이동된 카메라 방향 애니메이션 추가
        self.move_camera(
            phi=40 * DEGREES,
            theta=-120 * DEGREES,
            run_time=2
        )

        # 카메라 로테이션 시작
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(2.07)

    def tear_down(self):
        print("Tearing down the scene")
        super().tear_down()
