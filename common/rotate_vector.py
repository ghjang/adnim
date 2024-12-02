from manim import *
import numpy as np

# 상수 정의
DEFAULT_STROKE_WIDTH = 4
DEFAULT_TIP_LENGTH_RATIO = 0.15
DEFAULT_VECTOR_OPACITY = 1.0
DEFAULT_DOT_RADIUS = 0.05
DEFAULT_DOT_OPACITY = 1.2
DEFAULT_STROKE_OPACITY = 0.3

# 벡터 스타일 상수 추가
VECTOR_STYLE = {
    'stroke_width': 3,
    'tip_length': 0.2,
    'max_tip_length_to_length_ratio': 0.25
}

def create_rotated_vector(plane, direction, color, start_point=ORIGIN, **kwargs):
    """벡터 생성을 위한 헬퍼 함수"""
    # Vector 클래스 직접 사용하되 공통 스타일 적용
    vector = Vector(
        direction=direction,
        color=color,
        **VECTOR_STYLE  # 공통 스타일 적용
    ).shift(start_point)
    
    return vector


class BaseVectorAnimation(Animation):
    """벡터 애니메이션의 기본 클래스"""

    def __init__(self, mobject, plane, color=None, **kwargs):
        super().__init__(mobject, **kwargs)
        self.plane = plane
        self.color = color if color else mobject.get_color()
        self.center = mobject.get_start()
        # 벡터의 길이를 화면 좌표계가 아닌 논리적 좌표계에서 계산
        start = self.plane.plane.p2c(mobject.get_start())
        end = self.plane.plane.p2c(mobject.get_end())
        self.length = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        
        # 원본 벡터의 스타일 저장
        self.original_style = {
            'max_tip_length_to_length_ratio': mobject.max_tip_length_to_length_ratio,
            'tip_length': mobject.tip_length,
            'stroke_width': mobject.stroke_width
        }

    def create_vector_at_angle(self, angle, length=None):
        """주어진 각도에서 벡터 생성"""
        # length가 지정되지 않으면 원본 벡터의 길이 사용
        vector_length = length if length is not None else self.length
        # 논리적 좌표계에서 벡터 끝점 계산
        x = vector_length * np.cos(angle)
        y = vector_length * np.sin(angle)
        # 논리적 좌표를 화면 좌표로 변환
        vec_end = self.plane.plane.c2p(
            self.plane.plane.p2c(self.center)[0] + x,
            self.plane.plane.p2c(self.center)[1] + y
        )
        
        vector = Vector(
            direction=vec_end - self.center,
            color=self.color,
            **self.original_style  # 원본 스타일 적용
        ).shift(self.center)
        
        return vector


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
        # reference_circle이 제공된 경우, 해당 원의 중심과 반지름 설정
        if reference_circle:
            self.center = reference_circle.get_center()
            # 원의 반지름을 논리적 좌표계에서 계산
            center_point = self.plane.plane.p2c(reference_circle.get_center())
            radius_point = self.plane.plane.p2c(reference_circle.get_start())
            self.length = abs(radius_point[0] - center_point[0])

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
        show_end_dot=True,
        end_dot_color=None,
        end_dot_radius=0.05,
        stroke_width=2,
        **kwargs
    ):
        # VGroup으로 선과 점을 함께 관리
        result_group = VGroup()
        
        # 시작점에서 시작점으로 향하는 선으로 초기화
        start_point = start_vector.get_start()
        resultant = Line(
            start=start_point,
            end=start_point,
            color=color,
            stroke_width=stroke_width
        )
        resultant.set_stroke(opacity=stroke_opacity)
        result_group.add(resultant)
        
        # 종점 표시가 활성화된 경우에만 점 생성
        if show_end_dot:
            dot_color = end_dot_color if end_dot_color else color
            end_dot = Dot(
                point=start_point,
                color=dot_color,
                radius=end_dot_radius
            ).set_opacity(stroke_opacity * 1.2)  # 점은 선보다 약간 더 진하게
            result_group.add(end_dot)
        else:
            end_dot = None
            
        super().__init__(result_group, **kwargs)
        
        self.resultant = resultant
        self.end_dot = end_dot
        self.start_vector = start_vector
        self.end_vector = end_vector
        self.stroke_opacity = stroke_opacity

    def interpolate_mobject(self, alpha):
        start_point = self.start_vector.get_start()
        end_point = self.end_vector.get_end()
        
        # 선의 시작점과 끝점을 업데이트
        self.resultant.put_start_and_end_on(start_point, end_point)
        
        if self.end_dot:
            self.end_dot.move_to(end_point)
