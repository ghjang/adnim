from manim import *
from common.number_plane_group import *
from common.animation.rotate_vector import RotateVector


def create_unit_circle(plane, center_point=(0, 0), color=BLUE):
    """단위원 생성 헬퍼 함수"""
    return plane.add_circle(
        center_point=center_point,
        radius=1,
        color=color,
        stroke_width=2,
        fill_opacity=0.1
    )


def create_radius_vector(plane, target_circle, initial_angle, color, name=None):
    """Helper function to create radius vector

    Args:
        plane: NumberPlaneGroup object
        target_circle: Circle object that this vector will be radius of
        initial_angle: Starting angle in radians
        color: Vector color (str or RGB value)
        name: Name of the vector (optional)

    Returns:
        Vector: A radius vector with specified angle and color
    """
    center_point = plane.plane.p2c(target_circle.get_center())
    x = np.cos(initial_angle)
    y = np.sin(initial_angle)
    return plane.add_vector(
        vec=(x, y),
        name=name,  # 이름 파라미터 전달
        color=color,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.15,
        start_point=center_point
    )


def get_next_vector(plane, pattern="vector_.*"):
    """이름 패턴으로 벡터를 찾는 헬퍼 함수"""
    vectors = list(plane.iter_mobjects(
        name_pattern=pattern, obj_type=MobjectType.VECTOR))
    return vectors[0] if vectors else None


class UnitCircle(Scene):
    def construct(self):
        npg = NumberPlaneGroup().scale(4)
        self.play(FadeIn(npg))

        unit_circle = create_unit_circle(npg)
        self.play(FadeIn(unit_circle))

        radius_vector = create_radius_vector(npg, unit_circle, 0, RED)
        self.play(FadeIn(radius_vector))

        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
        ).scale(0.75).to_edge(LEFT)

        self.play(Transform(npg, new_npg))

        self.wait(3)


class UnitCircleWithAngle(Scene):
    def construct(self):
        npg = NumberPlaneGroup().scale(4)
        self.play(FadeIn(npg))

        unit_circle = create_unit_circle(npg)
        self.play(FadeIn(unit_circle))

        radius_vector = create_radius_vector(npg, unit_circle, PI / 2, GREEN)
        self.play(FadeIn(radius_vector))

        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
        ).scale(0.75).to_edge(LEFT)

        self.play(Transform(npg, new_npg))

        self.wait(3)


class UnitCircleWithRotation(Scene):
    def construct(self):
        npg = NumberPlaneGroup().scale(4)
        self.play(FadeIn(npg))

        unit_circle = create_unit_circle(npg)
        self.play(FadeIn(unit_circle))

        radius_vector = create_radius_vector(npg, unit_circle, PI / 2, GREEN)
        self.play(FadeIn(radius_vector))

        # 변환된 좌표계 생성
        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
        ).scale(0.75).to_edge(LEFT)

        self.play(ReplacementTransform(npg, new_npg))

        radius_vector = get_next_vector(new_npg)

        self.play(
            RotateVector(
                radius_vector,
                new_npg,
                angle_range=(PI / 2, PI / 2 + 2 * PI),
                run_time=4,
                rate_func=linear
            )
        )

        self.wait(1)


class UnitCircleWithRotation1(Scene):
    def construct(self):
        npg = NumberPlaneGroup(
            origin_config={
                "style": OriginStyle.CROSS
            }
        ).scale(4)
        self.play(FadeIn(npg))

        unit_circle_0 = create_unit_circle(npg)
        self.play(FadeIn(unit_circle_0))

        radius_vector_0 = create_radius_vector(
            npg, unit_circle_0, PI / 2, GREEN)
        self.play(FadeIn(radius_vector_0))

        # 변환된 좌표계 생성
        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
        ).scale(0.75).to_edge(LEFT)

        self.play(ReplacementTransform(npg, new_npg))

        radius_vector_0 = get_next_vector(new_npg)

        self.play(
            RotateVector(
                radius_vector_0,
                new_npg,
                angle_range=(PI / 2, PI / 2 + 2 * PI),
                run_time=4,
                rate_func=linear
            )
        )

        self.wait(1)


class UnitCircleWithPairRotation(Scene):
    def construct(self):
        npg = NumberPlaneGroup().scale(4)
        self.play(FadeIn(npg))

        unit_circle_0 = create_unit_circle(
            npg,
            center_point=(0, 0),
            color=BLUE
        )
        unit_circle_1 = create_unit_circle(
            npg,
            center_point=(1, 0),
            color=PURPLE
        )
        self.play(
            FadeIn(unit_circle_0),
            FadeIn(unit_circle_1)
        )

        radius_vector_0 = create_radius_vector(
            npg,
            unit_circle_0,
            0,
            GREEN,
            "radius_vector_0"
        )
        radius_vector_1 = create_radius_vector(
            npg,
            unit_circle_1,
            PI / 2,
            GREEN,
            "radius_vector_1"
        )
        self.play(
            FadeIn(radius_vector_0),
            FadeIn(radius_vector_1)
        )

        # 변환된 좌표계 생성
        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 3, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=4,
        ).scale(0.75).to_edge(LEFT)

        self.play(ReplacementTransform(npg, new_npg))

        vector_0 = get_next_vector(new_npg, "radius_vector_0")
        vector_1 = get_next_vector(new_npg, "radius_vector_1")

        self.play(
            RotateVector(
                vector_0,
                new_npg,
                angle_range=(0, 2 * PI),
                rate_func=linear
            ),
            RotateVector(
                vector_1,
                new_npg,
                angle_range=(PI / 2, PI / 2 + 2 * PI),
                rate_func=linear
            ),
            run_time=4
        )

        self.wait(1)
