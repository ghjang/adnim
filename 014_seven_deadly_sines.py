from manim import *
from common.number_plane_group import *
from common.create_with_tracer import *
from common.rotate_vector import *


def create_unit_circle(plane, center_point=(0, 0), color=BLUE, name=None):
    """단위원 생성 헬퍼 함수"""
    return plane.add_circle(
        center_point=center_point,
        radius=1,
        color=color,
        stroke_width=2,
        fill_opacity=0.1,
        name=name  # 이름 추가
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


class UnitCircleWithPairRotation(Scene):
    def construct(self):
        npg = NumberPlaneGroup().scale(4)
        self.play(FadeIn(npg))

        unit_circle_0 = create_unit_circle(
            npg,
            center_point=(0, 0),
            color=BLUE,
            name="circle_0"  # 이름 추가
        )
        self.play(FadeIn(unit_circle_0))

        radius_vector_0 = create_radius_vector(
            npg,
            unit_circle_0,
            0,
            TEAL,          # 청록색 - BLUE 원과 조화를 이루면서 눈에 잘 띔
            "radius_vector_0"
        )
        self.play(FadeIn(radius_vector_0))

        unit_circle_1 = create_unit_circle(
            npg,
            center_point=(1, 0),
            color=PURPLE,
            name="circle_1"  # 이름 추가
        )
        self.play(FadeIn(unit_circle_1))

        radius_vector_1 = create_radius_vector(
            npg,
            unit_circle_1,
            0,
            PINK,          # 분홍색 - PURPLE 원과 잘 어울림
            "radius_vector_1"
        )
        self.play(FadeIn(radius_vector_1))

        # 변환된 좌표계 생성
        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
        ).scale(0.9).to_edge(LEFT, buff=1.5)

        self.play(ReplacementTransform(npg, new_npg))

        # 함수식 라벨 추가 - 각 항별로 색상 다르게 지정
        formula = MathTex(
            r"\sin(x)", "+", r"\sin(2x)",
            tex_to_color_map={
                r"\sin(x)": TEAL,    # 첫 번째 항은 첫 번째 원의 벡터 색상
                r"\sin(2x)": PINK    # 두 번째 항은 두 번째 원의 벡터 색상
            }
        ).scale(0.8)
        formula.next_to(new_npg, DOWN, buff=0.5)
        self.play(FadeIn(formula))

        plot_npg = NumberPlaneGroup(
            x_range=[-1, 2 * PI, 1],
            y_range=[-3, 3, 1],
            x_length=1 + 2 * PI,
            y_length=3 + 3,
        ).scale(0.9).to_edge(RIGHT, buff=1.5)

        self.play(FadeIn(plot_npg))

        vector_0 = get_next_vector(new_npg, "radius_vector_0")
        vector_1 = get_next_vector(new_npg, "radius_vector_1")

        # NumberPlaneGroup에서 circle_1을 찾아서 애니메이션에 사용
        circle_1 = new_npg.find_mobject("circle_1", MobjectType.CIRCLE)

        sine_plot = plot_npg.plot_function(
            lambda x: np.sin(x) + np.sin(2 * x),
            x_range=[0, 2 * PI],
            color=RED
        )

        self.play(
            RotateVectorWithAngularVelocity(
                vector_0,
                new_npg,
                initial_angle=0,
                angular_velocity=1,
                n_revolutions=1,
                reference_circle=new_npg.find_mobject(
                    "circle_0", MobjectType.CIRCLE),  # circle_0도 찾아서 사용
                rate_func=linear
            ),
            RotateVectorWithAngularVelocity(
                vector_1,
                new_npg,
                initial_angle=0,
                angular_velocity=2,      # 2배 빠른 속도
                n_revolutions=1,
                reference_circle=circle_1,  # 두 번째 원을 기준으로
                rate_func=linear
            ),
            UpdateVectorWithCircle(
                vector_1,
                circle_1,
                vector_0,
                rate_func=linear
            ),
            ShowResultantVector(
                new_npg,
                vector_0,
                vector_1,
                color=YELLOW,
                stroke_opacity=0.3,
                show_end_dot=True,
                end_dot_color=RED,
                end_dot_radius=0.05,
                rate_func=linear
            ),
            CreateWithTracer(sine_plot, rate_func=linear, tracer_config={
                "cross_lines": True,
                "show_v_line": True,
                "screen_fixed_lines": True,
                "fixed_x_range": [-4*PI, 4*PI]
            }),
            run_time=8
        )

        self.wait(2)
