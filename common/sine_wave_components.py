
from manim import *
from dataclasses import dataclass
from typing import Tuple, Optional, List, Callable
from .number_plane_group import *
from .rotate_vector import *


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
            animations.append(
                RotateVectorWithAngularVelocity(
                    vector,
                    self.plane,
                    initial_angle=0,
                    angular_velocity=i + 1,
                    n_revolutions=n_revolutions,
                    reference_circle=circle,
                    rate_func=linear
                )
            )

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


def create_sum_function(n_components: int) -> Callable[[float], float]:
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
