from typing import override
from manim import *
from base_rotation import BaseRotation, BraceConfig


class CosineRotation(BaseRotation):
    """단위원에서 '코싸인 활꼴 회전'을 시각화하는 애니메이션"""

    @override
    def trig_name(self) -> str:
        return "cosine"

    @override
    def before_begin(self):
        self.base_unit_circle.add_shapes_for_cosine()

    @override
    def after_finish(self):
        if self.remove_shapes:
            self.base_unit_circle.remove_shapes_for_cosine()

    @override
    def update_main_objects_state(self, alpha, current_angle):
        plane = self.base_unit_circle.plane

        # 현재 시점 회전각 위치에서의 단위원 상을 이동하는 점의 좌표 계산
        x = np.cos(current_angle)
        y = np.sin(current_angle)

        # 평면 좌표로 변환
        origin = plane.c2p(0, 0)
        circle_point = plane.c2p(x, y)
        y_point = plane.c2p(0, y)  # cosine은 y축 기준점

        # 삼각형 업데이트
        triangle_points = [origin, circle_point, y_point, origin]
        left_points = [
            origin,
            plane.c2p(-x, y),  # x좌표 반전
            y_point,
            origin
        ]

        # 우측 삼각형
        self.base_unit_circle\
            .right_triangle\
            .set_points_as_corners(triangle_points)

        # 좌측 삼각형
        self.base_unit_circle\
            .left_triangle\
            .set_points_as_corners(left_points)

        # '피처 현' 업데이트
        self.base_unit_circle\
            .right_half_chord\
            .set_points_by_ends(circle_point, y_point)
        self.base_unit_circle\
            .left_half_chord\
            .set_points_by_ends(plane.c2p(-x, y), y_point)

        # 점 업데이트
        self.base_unit_circle.right_dot.move_to(circle_point)
        self.base_unit_circle.left_dot.move_to(plane.c2p(-x, y))

        # 브레이스 표시 여부에 따라 처리
        self._update_brace_config(alpha, x, y)

    def _update_brace_config(self, alpha, x, y):
        self.brace_config = None

        # 현재 좌표계의 스케일을 고려한 최소 너비 계산
        unit_x_width = abs(
            self.base_unit_circle.plane.c2p(1, 0)[0]
            - self.base_unit_circle.plane.c2p(0, 0)[0]
        )

        circle_point_width = abs(x)
        min_width = 0.1 * unit_x_width

        # 브레이스 표시 여부 플래그 설정:
        # - 첫번째 프레임에서는 브레이스를 표시하지 않음
        # - 'cos 값(=현의 너비)'이 너무 작을 때도 브레이스를 표시하지 않음
        show_brace_for_frame = alpha > 0 and circle_point_width > min_width

        if show_brace_for_frame:
            self.brace_config = BraceConfig(
                ref_obj=self.base_unit_circle.right_half_chord,
                direction=UP if y >= 0 else DOWN,
                text="\\cos(x)"
            )
