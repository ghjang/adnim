from manim import *


class VectorSum(Scene):
    def construct(self):
        self.next_section("Sum of Two Planar Vectors Intro")

        addition_title = Text("Sum of Two Planar Vectors",
                              font="Montserrat").scale(1.5)
        addition_title.set_color_by_gradient(
            RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        addition_title.to_edge(UP)
        self.add(addition_title)

        plus_text = Text("+", font="Montserrat").scale(2).shift(DOWN / 2)
        v1 = Vector([2, 3], color=RED).next_to(
            plus_text, LEFT, buff=1.5).set_z_index(9000)
        v2 = Vector([3, 0], color=BLUE).next_to(
            plus_text, RIGHT, buff=1.5).set_z_index(9000)
        self.add(plus_text, v1, v2)

        self.wait(1)

        self.next_section("Moving the Vectors to 2D Plane")

        number_plane = NumberPlane(
            background_line_style={
                "stroke_opacity": 0.5
            }
        )
        origin_dot = Dot(color=WHITE).set_z_index(
            9999) .move_to(number_plane.coords_to_point(0, 0))

        self.play(
            FadeOut(addition_title),
            FadeOut(plus_text),
            FadeIn(number_plane),
            v1.animate.set_z_index(9998),
            v2.animate.set_z_index(9998),
            FadeIn(origin_dot),
            run_time=2
        )

        self.play(
            v1.animate.shift(number_plane.c2p(0, 0) - v1.get_start()),
            v2.animate.shift(number_plane.c2p(0, 0) - v2.get_start()),
            run_time=1
        )

        self.wait(1)

        self.next_section("Moving the Number Plane to the Left-Down")

        # NOTE: 'NumberPlane'의 'x_range'와 'y_range'의 변경은 '생성자'에서만 가능함.
        left_down_point = LEFT * 2 + DOWN
        self.play(
            number_plane.animate.shift(left_down_point),
            origin_dot.animate.shift(left_down_point),
            v1.animate.shift(left_down_point),
            v2.animate.shift(left_down_point),
            Transform(number_plane, NumberPlane(
                x_range=[-6, 10],   # 영역 넓이 16 유지
                y_range=[-3, 5],    # 영역 넓이 8 유지
                background_line_style={
                    "stroke_opacity": 0.5
                }
            )
            ),
            run_time=1
        )

        v1_label = MathTex(r"\vec{v_1}", color=RED).next_to(
            v1, LEFT).shift(RIGHT + UP)
        v2_label = MathTex(r"\vec{v_2}", color=BLUE).next_to(v2, DOWN)
        self.play(
            Write(v1_label),
            Write(v2_label)
        )

        self.next_section("copying v2 and move it to v1's end point")

        # 위치 계산
        move_vector = v1.get_end() - v2.get_start()

        # 1. v2 복제
        v2_copy = v2.copy()

        # 2. 복제본 이동
        self.play(
            v2_copy.animate.shift(move_vector),
            run_time=1
        )

        # 3. 점선 스타일의 벡터 생성
        dashed_v2 = DashedVMobject(
            Vector(
                v2.get_vector(),
                tip_length=0,   # '화살촉' 제거
                color=WHITE,
                stroke_opacity=0.5
            ).shift(v1.get_end())
        )

        # 4. Transform 실행
        self.play(
            Transform(v2_copy, dashed_v2),
            run_time=0.5
        )

        self.next_section("Add the result addition vector")

        # 현재 numberplane의 원점 위치
        # plane_origin = number_plane.c2p(0, 0)
        plane_origin = left_down_point

        # v_sum 벡터 생성 및 위치 조정
        v_sum = Vector(
            v1.get_vector() + v2.get_vector(),
            color=GREEN
        )

        v_sum.shift(plane_origin - v_sum.get_start())

        # v_sum 추가
        self.play(
            Create(v_sum),
            run_time=1.5
        )

        v_sum_label = MathTex(
            r"\vec{v_1} + \vec{v_2}",
            color=GREEN
        ).next_to(v_sum, RIGHT).shift(LEFT * 2)
        self.play(Write(v_sum_label))

        self.wait(2)


class VectorDiff(Scene):
    def construct(self):
        self.next_section(
            "Difference of Two Planar Vectors Intro")

        diff_title = Text("Difference of Two Planar Vectors",
                          font="Montserrat").scale(1.3)
        diff_title.set_color_by_gradient(
            RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        diff_title.to_edge(UP)
        self.add(diff_title)

        minus_text = Text("-", font="Montserrat").scale(2).shift(DOWN / 2)
        v1 = Vector([2, 3], color=RED).next_to(
            minus_text, LEFT, buff=1.5).set_z_index(9000)
        v2 = Vector([3, 0], color=BLUE).next_to(
            minus_text, RIGHT, buff=1.5).set_z_index(9000)
        self.add(minus_text, v1, v2)

        self.wait(1)

        self.next_section("Moving the Vectors to 2D Plane")

        number_plane = NumberPlane(
            background_line_style={
                "stroke_opacity": 0.5
            }
        )
        origin_dot = Dot(color=WHITE).set_z_index(
            9999).move_to(number_plane.coords_to_point(0, 0))

        self.play(
            FadeOut(diff_title),
            FadeOut(minus_text),
            FadeIn(number_plane),
            v1.animate.set_z_index(9998),
            v2.animate.set_z_index(9998),
            FadeIn(origin_dot),
            run_time=2
        )

        self.play(
            v1.animate.shift(number_plane.c2p(0, 0) - v1.get_start()),
            v2.animate.shift(number_plane.c2p(0, 0) - v2.get_start()),
            run_time=1
        )

        self.wait(1)

        self.next_section("Moving the Number Plane to the Down")

        down_point = DOWN
        self.play(
            number_plane.animate.shift(down_point),
            origin_dot.animate.shift(down_point),
            v1.animate.shift(down_point),
            v2.animate.shift(down_point),
            Transform(number_plane, NumberPlane(
                x_range=[-8, 8],
                y_range=[-3, 5],
                background_line_style={
                    "stroke_opacity": 0.5
                }
            )),
            run_time=1
        )

        v1_label = MathTex(r"\vec{v_1}", color=RED).next_to(
            v1, RIGHT).shift(LEFT * 0.7)
        v2_label = MathTex(r"\vec{v_2}", color=BLUE).next_to(v2, DOWN)
        self.play(
            Write(v1_label),
            Write(v2_label)
        )

        self.next_section("Add -v2")

        # -v2 벡터 생성
        v2_neg = Vector(-v2.get_vector(), color=BLUE)

        # 이동된 numberplane의 원점으로 이동 (down_point 사용)
        v2_neg.shift(down_point)

        # 생성 애니메이션
        self.play(
            Create(v2_neg),
            run_time=1
        )

        v2_neg_label = MathTex(r"-\vec{v_2}", color=BLUE).next_to(v2_neg, DOWN)
        self.play(Write(v2_neg_label))

        self.next_section("Move -v2's copy to v1's end point")

        v2_neg_copy = v2_neg.copy()

        # v1의 끝점으로 이동 애니메이션
        self.play(
            v2_neg_copy.animate.shift(v1.get_end() - v2_neg.get_start()),
            run_time=1
        )

        # 점선 스타일의 벡터 생성
        dashed_v2_neg = DashedVMobject(
            Vector(
                v2_neg.get_vector(),
                tip_length=0,   # '화살촉' 제거
                color=WHITE,
                stroke_opacity=0.5
            ).shift(v1.get_end())
        )

        # Transform 실행
        self.play(
            Transform(v2_neg_copy, dashed_v2_neg),
            run_time=0.5
        )

        self.next_section("Add the result difference vector")

        plane_origin = down_point

        v_diff = Vector(
            v1.get_vector() - v2.get_vector(),
            color=GREEN
        )

        v_diff.shift(plane_origin - v_diff.get_start())

        self.play(
            Create(v_diff),
            run_time=1.5
        )

        v_diff_label = MathTex(
            r"\vec{v_1} - \vec{v_2}",
            color=GREEN
        ).next_to(v_diff, LEFT)
        self.play(Write(v_diff_label))

        self.wait(2)


class Vector3DSum(ThreeDScene):
    def construct(self):
        self.next_section("Sum of Two Spatial Vectors Intro")

        addition_title = Text("Sum of Two Spatial Vectors",
                              font="Montserrat").scale(1.5)
        addition_title.set_color_by_gradient(
            RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        addition_title.to_edge(UP)
        self.add(addition_title)

        plus_text = Text("+", font="Montserrat").scale(2).shift(DOWN / 2)
        v1 = Vector([2, 3, 1], color=RED).next_to(
            plus_text, LEFT, buff=1.5).set_z_index(9000)
        v2 = Vector([3, -1, 2], color=BLUE).next_to(
            plus_text, RIGHT, buff=1.5).set_z_index(9000)
        self.add(plus_text, v1, v2)

        self.wait(1)

        self.next_section("Moving the Vectors to 3D Plane")

        axes = ThreeDAxes()
        origin_dot = Dot(color=WHITE).set_z_index(
            9999).move_to(axes.c2p(0, 0, 0))

        self.play(
            FadeOut(addition_title),
            FadeOut(plus_text),
            FadeIn(axes),
            v1.animate.set_z_index(9998),
            v2.animate.set_z_index(9998),
            FadeIn(origin_dot),
            run_time=2
        )

        self.play(
            v1.animate.shift(axes.c2p(0, 0, 0) - v1.get_start()),
            v2.animate.shift(axes.c2p(0, 0, 0) - v2.get_start()),
            run_time=1
        )

        self.wait(1)

        self.next_section("Moving the Axes to the Left-Down")

        left_down_point = LEFT * 2 + DOWN
        self.play(
            axes.animate.shift(left_down_point),
            origin_dot.animate.shift(left_down_point),
            v1.animate.shift(left_down_point),
            v2.animate.shift(left_down_point),
            run_time=1
        )

        v1_label = MathTex(r"\vec{v_1}", color=RED).next_to(
            v1, LEFT).shift(RIGHT + UP)
        v2_label = MathTex(r"\vec{v_2}", color=BLUE).next_to(v2, DOWN)
        self.play(
            Write(v1_label),
            Write(v2_label)
        )

        self.next_section("Copying v2 and move it to v1's end point")

        move_vector = v1.get_end() - v2.get_start()
        v2_copy = v2.copy()

        self.play(
            v2_copy.animate.shift(move_vector),
            run_time=1
        )

        dashed_v2 = DashedVMobject(
            Vector(
                v2.get_vector(),
                tip_length=0,
                color=WHITE,
                stroke_opacity=0.5
            ).shift(v1.get_end())
        )

        self.play(
            Transform(v2_copy, dashed_v2),
            run_time=0.5
        )

        self.next_section("Add the result addition vector")

        plane_origin = left_down_point
        v_sum = Vector(
            v1.get_vector() + v2.get_vector(),
            color=GREEN
        )

        v_sum.shift(plane_origin - v_sum.get_start())

        self.play(
            Create(v_sum),
            run_time=1.5
        )

        v_sum_label = MathTex(
            r"\vec{v_1} + \vec{v_2}",
            color=GREEN
        ).next_to(v_sum, RIGHT).shift(LEFT * 2)
        self.play(Write(v_sum_label))

        self.wait(1)

        self.next_section("Add the plane formed by the two vectors")

        # 두 벡터가 형성하는 평면을 추가
        plane_vertices = [
            plane_origin,
            plane_origin + v1.get_vector(),
            plane_origin + v1.get_vector() + v2.get_vector(),
            plane_origin + v2.get_vector()
        ]
        plane = Polygon(*plane_vertices, color=YELLOW, fill_opacity=0.25)

        self.play(
            FadeIn(plane),
            run_time=1
        )

        self.wait(1)

        self.play(
            FadeOut(v1_label),
            FadeOut(v2_label),
            FadeOut(v_sum_label)
        )

        # 카메라 뷰를 틀어 3D 느낌을 더해줌
        self.move_camera(phi=100 * DEGREES, theta=-50 * DEGREES, run_time=3)
        self.wait(2)
 