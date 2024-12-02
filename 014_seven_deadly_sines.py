from manim import *
from common.number_plane_group import *
from common.create_with_tracer import *
from common.rotate_vector import *

# 상수 정의
MAIN_SCALE = 4
TRANSFORMED_SCALE = 0.9
FORMULA_SCALE = 0.8
ANIMATION_RUN_TIME = 8
LEFT_EDGE_BUFF = 1.5
RIGHT_EDGE_BUFF = 1.5

# 색상 설정
COLORS = {
    'CIRCLE_1': BLUE,
    'CIRCLE_2': PURPLE,
    'VECTOR_1': TEAL,
    'VECTOR_2': PINK,
    'RESULT_VECTOR': YELLOW,
    'END_DOT': RED,
    'PLOT': RED
}


def create_unit_circle(plane, center_point=(0, 0), color=BLUE, name=None):
    """단위원 생성 헬퍼 함수"""
    return plane.add_circle(
        center_point=center_point,
        radius=1,
        color=color,
        stroke_width=2,
        fill_opacity=0.1,
        name=name
    )


def create_radius_vector(plane, target_circle, initial_angle, color, name=None):
    """반지름 벡터 생성 헬퍼 함수"""
    center_point = plane.plane.p2c(target_circle.get_center())
    x = np.cos(initial_angle)
    y = np.sin(initial_angle)
    return plane.add_vector(
        vec=(x, y),
        name=name,
        color=color,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.15,
        start_point=center_point
    )


def get_next_vector(plane, pattern="vector_.*"):
    """이름 패턴으로 벡터를 찾는 헬퍼 함수"""
    vectors = list(plane.iter_mobjects(pattern, obj_type=MobjectType.VECTOR))
    return vectors[0] if vectors else None


def create_main_plane():
    """메인 좌표계 생성"""
    return NumberPlaneGroup().scale(MAIN_SCALE)


def create_transformed_plane(npg):
    """변환된 좌표계 생성"""
    return npg.copy_with_transformed_plane(
        x_range=[-2, 2, 1],
        y_range=[-2, 2, 1],
        x_length=4,
        y_length=4,
    ).scale(TRANSFORMED_SCALE).to_edge(LEFT, buff=LEFT_EDGE_BUFF)


def create_plot_plane():
    """플롯 좌표계 생성"""
    return NumberPlaneGroup(
        x_range=[-1, 2 * PI, 1],
        y_range=[-3, 3, 1],
        x_length=1 + 2 * PI,
        y_length=3 + 3,
    ).scale(TRANSFORMED_SCALE).to_edge(RIGHT, buff=RIGHT_EDGE_BUFF)


def create_formula():
    """수식 생성"""
    return MathTex(
        r"\sin(x)", "+", r"\sin(2x)",
        tex_to_color_map={
            r"\sin(x)": COLORS['VECTOR_1'],
            r"\sin(2x)": COLORS['VECTOR_2']
        }
    ).scale(FORMULA_SCALE)


def create_animations(new_npg, plot_npg, vector_0, vector_1, circle_1, sine_plot):
    """애니메이션 그룹 생성"""
    return [
        RotateVectorWithAngularVelocity(
            vector_0,
            new_npg,
            initial_angle=0,
            angular_velocity=1,
            n_revolutions=1,
            reference_circle=new_npg.find_mobject(
                "circle_0", MobjectType.CIRCLE),
            rate_func=linear
        ),
        RotateVectorWithAngularVelocity(
            vector_1,
            new_npg,
            initial_angle=0,
            angular_velocity=2,
            n_revolutions=1,
            reference_circle=circle_1,
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
            color=COLORS['RESULT_VECTOR'],
            stroke_opacity=0.3,
            show_end_dot=True,
            end_dot_color=COLORS['END_DOT'],
            end_dot_radius=0.05,
            rate_func=linear
        ),
        CreateWithTracer(sine_plot, rate_func=linear, tracer_config={
            "cross_lines": True,
            "show_v_line": True,
            "screen_fixed_lines": True,
            "fixed_x_range": [-4*PI, 4*PI]
        })
    ]


class SumOfTwoSine(Scene):
    def construct(self):
        # 초기 좌표계 생성 및 표시
        npg = create_main_plane()
        self.play(FadeIn(npg))

        # 첫 번째 원과 벡터 생성
        unit_circle_0 = create_unit_circle(
            npg, color=COLORS['CIRCLE_1'], name="circle_0")
        self.play(FadeIn(unit_circle_0))

        radius_vector_0 = create_radius_vector(
            npg, unit_circle_0, 0, COLORS['VECTOR_1'], "radius_vector_0")
        self.play(FadeIn(radius_vector_0))

        # 두 번째 원과 벡터 생성
        unit_circle_1 = create_unit_circle(
            npg, center_point=(1, 0), color=COLORS['CIRCLE_2'], name="circle_1")
        self.play(FadeIn(unit_circle_1))

        radius_vector_1 = create_radius_vector(
            npg, unit_circle_1, 0, COLORS['VECTOR_2'], "radius_vector_1")
        self.play(FadeIn(radius_vector_1))

        # 변환된 좌표계로 전환
        new_npg = create_transformed_plane(npg)
        self.play(ReplacementTransform(npg, new_npg))

        # 수식 추가
        formula = create_formula()
        formula.next_to(new_npg, DOWN, buff=0.5)
        self.play(FadeIn(formula))

        # 플롯 좌표계 생성
        plot_npg = create_plot_plane()
        self.play(FadeIn(plot_npg))

        # 벡터와 원 참조 가져오기
        vector_0 = get_next_vector(new_npg, "radius_vector_0")
        vector_1 = get_next_vector(new_npg, "radius_vector_1")
        circle_1 = new_npg.find_mobject("circle_1", MobjectType.CIRCLE)

        # 사인 플롯 생성
        sine_plot = plot_npg.plot_function(
            lambda x: np.sin(x) + np.sin(2 * x),
            x_range=[0, 2 * PI],
            color=COLORS['PLOT']
        )

        # 애니메이션 실행
        self.play(
            *create_animations(new_npg, plot_npg, vector_0,
                               vector_1, circle_1, sine_plot),
            run_time=ANIMATION_RUN_TIME
        )

        self.wait(2)
