from manim import *
import numpy as np


class RotateVector(Animation):
    """벡터 회전 애니메이션 클래스"""

    def __init__(
        self,
        mobject,
        plane,
        angle_range=(0, 2*PI),
        color=None,
        **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.plane = plane
        self.start_angle = angle_range[0]
        self.angle_diff = angle_range[1] - angle_range[0]
        if color is None:
            self.color = mobject.get_color()
        else:
            self.color = color
        # 시작점 저장
        self.center = mobject.get_start()

    def interpolate_mobject(self, alpha):
        angle = self.start_angle + self.angle_diff * alpha
        x = np.cos(angle)
        y = np.sin(angle)
        # 시작점을 기준으로 벡터 생성
        new_vector = Vector(
            direction=self.plane.plane.c2p(x, y) - self.plane.plane.c2p(0, 0),
            color=self.color,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        ).shift(self.center)  # 저장된 시작점으로 이동
        self.mobject.become(new_vector)


class RotateVectorWithAngularVelocity(Animation):
    """각속도 기반 벡터 회전 애니메이션 클래스"""

    def __init__(
        self,
        mobject,
        plane,
        initial_angle=0,      # 시작 각도
        angular_velocity=1,    # 상대적 회전 속도 (비율)
        n_revolutions=1,      # 총 회전 수
        reference_circle=None, # 기준이 되는 원 객체 (optional)
        color=None,
        **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.plane = plane
        self.initial_angle = initial_angle
        self.angular_velocity = angular_velocity  # 상대적 회전 속도
        self.total_angle = n_revolutions * TAU   # 전체 회전할 각도
        
        # 회전 중심점 설정
        if reference_circle:
            self.center = reference_circle.get_center()
        else:
            self.center = mobject.get_start()

        if color is None:
            self.color = mobject.get_color()
        else:
            self.color = color

    def interpolate_mobject(self, alpha):
        # alpha(0~1)에 angular_velocity를 곱해서 상대적 회전 속도 적용
        current_angle = self.initial_angle + \
            (self.total_angle * self.angular_velocity * alpha)

        x = np.cos(current_angle)
        y = np.sin(current_angle)
        new_vector = Vector(
            direction=self.plane.plane.c2p(x, y) - self.plane.plane.c2p(0, 0),
            color=self.color,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        ).shift(self.center)
        self.mobject.become(new_vector)


class UpdateVectorWithCircle(Animation):
    """원과 벡터를 함께 움직이는 애니메이션 클래스"""
    
    def __init__(
        self,
        vector,             # 움직일 벡터
        circle,             # 움직일 원
        reference_vector,   # 참조할 벡터 (끝점을 따라감)
        **kwargs
    ):
        super().__init__(vector, **kwargs)
        self.vector = vector
        self.circle = circle
        self.reference_vector = reference_vector

    def interpolate_mobject(self, alpha):
        # reference_vector의 현재 끝점 위치 가져오기
        end_point = self.reference_vector.get_end()
        # 원의 중심을 reference_vector의 끝점으로 이동
        self.circle.move_to(end_point)
        # 벡터의 시작점을 원의 중심으로 이동
        self.vector.shift(end_point - self.vector.get_start())


class ShowResultantVector(Animation):
    """두 벡터의 합을 보여주는 애니메이션 클래스"""
    
    def __init__(
        self,
        plane,
        start_vector,    # 시작 벡터
        end_vector,      # 끝 벡터
        color=YELLOW,    # 합 벡터의 색상
        stroke_opacity=0.3,  # 선 투명도
        show_end_dot=False,  # 종점 표시 여부
        end_dot_color=None,  # 종점 색상 (None이면 벡터와 같은 색)
        end_dot_radius=0.08, # 종점 크기
        **kwargs
    ):
        # VGroup으로 벡터와 점을 함께 관리
        result_group = VGroup()
        
        # 합 벡터 생성
        resultant = Vector(
            direction=[0, 0, 0],
            color=color,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )
        resultant.set_stroke(opacity=stroke_opacity)
        result_group.add(resultant)
        
        # 종점 표시가 활성화된 경우에만 점 생성
        if show_end_dot:
            dot_color = end_dot_color if end_dot_color is not None else color
            end_dot = Dot(
                point=[0, 0, 0],
                color=dot_color,
                radius=end_dot_radius
            ).set_opacity(stroke_opacity * 1.2)
            result_group.add(end_dot)
        else:
            end_dot = None
            
        super().__init__(result_group, **kwargs)
        
        self.plane = plane
        self.start_vector = start_vector
        self.end_vector = end_vector
        self.resultant = resultant
        self.end_dot = end_dot

    def interpolate_mobject(self, alpha):
        start_point = self.start_vector.get_start()
        end_point = self.end_vector.get_end()
        
        # 벡터 업데이트
        self.resultant.put_start_and_end_on(start_point, end_point)
        
        # 종점 점 업데이트 (존재하는 경우에만)
        if self.end_dot:
            self.end_dot.move_to(end_point)