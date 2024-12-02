from manim import *
import numpy as np

# 상수 정의
DEFAULT_STROKE_WIDTH = 4
DEFAULT_TIP_LENGTH_RATIO = 0.15
DEFAULT_VECTOR_OPACITY = 1.0
DEFAULT_DOT_RADIUS = 0.05
DEFAULT_DOT_OPACITY = 1.2
DEFAULT_STROKE_OPACITY = 0.3


def create_rotated_vector(plane, direction, color, start_point=ORIGIN, **kwargs):
    """벡터 생성을 위한 헬퍼 함수"""
    return Vector(
        direction=direction,
        color=color,
        stroke_width=kwargs.get('stroke_width', DEFAULT_STROKE_WIDTH),
        max_tip_length_to_length_ratio=kwargs.get(
            'max_tip_length_ratio', DEFAULT_TIP_LENGTH_RATIO)
    ).shift(start_point)


class BaseVectorAnimation(Animation):
    """벡터 애니메이션의 기본 클래스"""

    def __init__(self, mobject, plane, color=None, **kwargs):
        super().__init__(mobject, **kwargs)
        self.plane = plane
        self.color = color if color else mobject.get_color()
        self.center = mobject.get_start()

    def create_vector_at_angle(self, angle, length=1):
        """주어진 각도에서 벡터 생성"""
        x = length * np.cos(angle)
        y = length * np.sin(angle)
        return create_rotated_vector(
            self.plane,
            self.plane.plane.c2p(x, y) - self.plane.plane.c2p(0, 0),
            self.color,
            self.center
        )


class RotateVector(BaseVectorAnimation):
    """벡터 회전 애니메이션 클래스"""

    def __init__(self, mobject, plane, angle_range=(0, 2*PI), **kwargs):
        super().__init__(mobject, plane, **kwargs)
        self.start_angle = angle_range[0]
        self.angle_diff = angle_range[1] - angle_range[0]

    def interpolate_mobject(self, alpha):
        angle = self.start_angle + self.angle_diff * alpha
        new_vector = self.create_vector_at_angle(angle)
        self.mobject.become(new_vector)


class RotateVectorWithAngularVelocity(BaseVectorAnimation):
    """각속도 기반 벡터 회전 애니메이션 클래스"""

    def __init__(
        self,
        mobject,
        plane,
        initial_angle=0,
        angular_velocity=1,
        n_revolutions=1,
        reference_circle=None,
        **kwargs
    ):
        super().__init__(mobject, plane, **kwargs)
        self.initial_angle = initial_angle
        self.angular_velocity = angular_velocity
        self.total_angle = n_revolutions * TAU
        self.center = reference_circle.get_center(
        ) if reference_circle else mobject.get_start()

    def interpolate_mobject(self, alpha):
        current_angle = self.initial_angle + \
            (self.total_angle * self.angular_velocity * alpha)
        new_vector = self.create_vector_at_angle(current_angle)
        self.mobject.become(new_vector)


class UpdateVectorWithCircle(Animation):
    """원과 벡터를 함께 움직이는 애니메이션 클래스"""

    def __init__(self, vector, circle, reference_vector, **kwargs):
        super().__init__(vector, **kwargs)
        self.vector = vector
        self.circle = circle
        self.reference_vector = reference_vector

    def interpolate_mobject(self, alpha):
        end_point = self.reference_vector.get_end()
        self.circle.move_to(end_point)
        self.vector.shift(end_point - self.vector.get_start())


class ShowResultantVector(Animation):
    """두 벡터의 합을 보여주는 애니메이션 클래스"""

    def __init__(
        self,
        plane,
        start_vector,
        end_vector,
        color=YELLOW,
        stroke_opacity=0.3,
        show_end_dot=False,
        end_dot_color=None,
        end_dot_radius=0.05,
        **kwargs
    ):
        # VGroup으로 벡터와 점을 함께 관리
        result_group = VGroup()

        # 합 벡터 생성 방식 수정
        resultant = Vector(
            direction=[0, 0, 0],
            color=color,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        ).set_stroke(opacity=stroke_opacity)  # 투명도를 stroke에 직접 적용
        result_group.add(resultant)

        # 종점 표시가 활성화된 경우에만 점 생성
        if show_end_dot:
            dot_color = end_dot_color if end_dot_color else color
            end_dot = Dot(
                point=[0, 0, 0],
                color=dot_color,
                radius=end_dot_radius
            ).set_opacity(stroke_opacity * 1.2)  # 점의 투명도 조정
            result_group.add(end_dot)

        super().__init__(result_group, **kwargs)

        self.resultant = resultant
        self.end_dot = end_dot if show_end_dot else None
        self.start_vector = start_vector
        self.end_vector = end_vector

    def interpolate_mobject(self, alpha):
        start_point = self.start_vector.get_start()
        end_point = self.end_vector.get_end()

        # 벡터의 시작점과 끝점을 정확하게 설정
        self.resultant.put_start_and_end_on(start_point, end_point)

        if self.end_dot:
            self.end_dot.move_to(end_point)
