from manim import *
from common.number_plane_group import *
from common.create_with_tracer import *
from common.rotate_vector import *
from dataclasses import dataclass
from typing import Tuple, Optional

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


@dataclass
class RotationConfig:
    """회전 요소(원과 벡터) 설정"""
    center_point: Tuple[float, float]  # 원의 중심점
    angular_velocity: float            # 각속도
    color: str                        # 색상
    name_suffix: str                  # 이름 접미사
    initial_angle: float = 0          # 초기 각도


class SineWaveManager:
    """사인파 관리 클래스"""

    def __init__(self, plane: NumberPlaneGroup):
        self.plane = plane
        self.circles = []
        self.vectors = []

    def add_component(self, config: RotationConfig) -> Tuple[Circle, Vector]:
        """회전 요소 추가"""
        circle = create_unit_circle(
            self.plane,
            center_point=config.center_point,
            color=config.color,
            name=f"circle_{config.name_suffix}"
        )

        vector = create_radius_vector(
            self.plane,
            circle,
            config.initial_angle,
            config.color,
            f"radius_vector_{config.name_suffix}"
        )

        self.circles.append(circle)
        self.vectors.append(vector)
        return circle, vector

    def update_plane(self, new_plane: NumberPlaneGroup):
        """좌표계가 변경될 때 호출"""
        self.plane = new_plane
        # 기존 벡터와 원들의 reference를 새로운 plane에서 찾기
        self.circles = [
            new_plane.find_mobject(f"circle_{i}", MobjectType.CIRCLE)
            for i in range(len(self.circles))
        ]
        self.vectors = [
            new_plane.find_mobject(f"radius_vector_{i}", MobjectType.VECTOR)
            for i in range(len(self.vectors))
        ]

    def create_animations(self, n_revolutions: int = 1) -> list:
        """모든 회전 요소의 애니메이션 생성"""
        animations = []
        prev_vector = None

        for i, (circle, vector) in enumerate(zip(self.circles, self.vectors)):
            # 벡터 회전 애니메이션
            animations.append(
                RotateVectorWithAngularVelocity(
                    vector,
                    self.plane,
                    initial_angle=0,
                    angular_velocity=i + 1,  # 각속도는 1, 2, 3, ...
                    n_revolutions=n_revolutions,
                    reference_circle=circle,
                    rate_func=linear
                )
            )

            # 두 번째 원부터는 이전 벡터의 끝점을 따라다님
            if prev_vector:
                animations.append(
                    UpdateVectorWithCircle(
                        vector,
                        circle,
                        prev_vector,
                        rate_func=linear
                    )
                )

            prev_vector = vector

        return animations

    def create_resultant_animation(self, color=YELLOW) -> Animation:
        """합벡터 애니메이션 생성"""
        if len(self.vectors) < 2:
            return None

        return ShowResultantVector(
            self.plane,
            self.vectors[0],
            self.vectors[-1],
            color=color,
            stroke_opacity=0.3,
            show_end_dot=True,
            end_dot_color=RED,
            end_dot_radius=0.05,
            rate_func=linear
        )


def create_sum_function(n_components: int) -> callable:
    """n개 사인파의 합 함수 생성"""
    def sum_sine(x: float) -> float:
        return sum(np.sin((i + 1) * x) for i in range(n_components))
    return sum_sine


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


class SumOfTwoSine(Scene):
    def construct(self):
        # 초기 설정
        configs = [
            RotationConfig(
                center_point=(0, 0),
                angular_velocity=1,
                color=COLORS['CIRCLE_1'],
                name_suffix="0"
            ),
            RotationConfig(
                center_point=(1, 0),
                angular_velocity=2,
                color=COLORS['CIRCLE_2'],
                name_suffix="1"
            )
        ]

        # 초기 좌표계 생성 및 표시
        npg = create_main_plane()
        self.play(FadeIn(npg))

        # 회전 요소 관리자 생성
        manager = SineWaveManager(npg)

        # 회전 요소들 생성 및 표시
        for config in configs:
            circle, vector = manager.add_component(config)
            self.play(FadeIn(circle), FadeIn(vector))

        # 변환된 좌표계로 전환
        new_npg = create_transformed_plane(npg)
        self.play(ReplacementTransform(npg, new_npg))

        # 좌표계 변경 후 매니저 업데이트
        manager.update_plane(new_npg)

        # 수식 추가
        formula = create_formula()
        formula.next_to(new_npg, DOWN, buff=0.5)
        self.play(FadeIn(formula))

        # 플롯 좌표계 생성
        plot_npg = create_plot_plane()
        self.play(FadeIn(plot_npg))

        # 사인 플롯 생성
        sine_plot = plot_npg.plot_function(
            create_sum_function(len(configs)),
            x_range=[0, 2 * PI],
            color=COLORS['PLOT']
        )

        # 애니메이션 실행
        animations = [
            *manager.create_animations(),
            manager.create_resultant_animation(),
            CreateWithTracer(
                sine_plot,
                rate_func=linear,
                tracer_config={
                    "cross_lines": True,
                    "show_v_line": True,
                    "screen_fixed_lines": True,
                    "fixed_x_range": [-4*PI, 4*PI]
                }
            )
        ]

        self.play(*animations, run_time=ANIMATION_RUN_TIME)
        self.wait(2)
