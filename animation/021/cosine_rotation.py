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


class SecantRotation(BaseRotation):
    """단위원에서 '시컨트 회전'을 시각화하는 애니메이션"""

    @override
    def trig_name(self) -> str:
        return "secant"

    @override
    def before_begin(self):
        self.base_unit_circle.add_shapes_for_secant()

    @override
    def after_finish(self):
        if self.remove_shapes:
            self.base_unit_circle.remove_shapes_for_secant()

    @override
    def update_main_objects_state(self, alpha, current_angle):
        plane = self.base_unit_circle.plane

        # 1. 단위원 상의 점 계산
        x = np.cos(current_angle)
        y = np.sin(current_angle)

        circle_point = plane.c2p(x, y)

        # 2. x축 투영점 계산
        x_projection = plane.c2p(x, 0)

        # 3. 불연속점 체크 (90° 또는 270° 근처)
        EPSILON = 1e-3
        is_near_discontinuity = abs(abs(current_angle % PI) - PI/2) < EPSILON

        if is_near_discontinuity or abs(x) <= EPSILON:
            return

        # 4. x축과의 교점 계산 (sec = 1/cos)
        sec_x = 1 / x
        x_intercept = plane.c2p(sec_x, 0)

        # 모든 요소 기존 상태 유지하며 업데이트
        if self.base_unit_circle.secant_point:
            self.base_unit_circle.secant_point.move_to(circle_point)

        if self.base_unit_circle.secant_x_projection:
            self.base_unit_circle.secant_x_projection.move_to(x_projection)

        if self.base_unit_circle.secant_x_axis_intercept:
            self.base_unit_circle.secant_x_axis_intercept.move_to(x_intercept)

        if self.base_unit_circle.secant_radius:
            self.base_unit_circle.secant_radius.set_points_by_ends(
                plane.c2p(0, 0), circle_point)

        if self.base_unit_circle.secant_line:
            self.base_unit_circle.secant_line.set_points_by_ends(
                plane.c2p(0, 0), x_intercept)

        if self.base_unit_circle.secant_inner_triangle:
            self.base_unit_circle.secant_inner_triangle.set_points_as_corners([
                plane.c2p(0, 0),
                circle_point,
                x_projection,
                plane.c2p(0, 0)
            ])

        if self.base_unit_circle.secant_outer_triangle:
            self.base_unit_circle.secant_outer_triangle.set_points_as_corners([
                circle_point,
                x_projection,
                x_intercept,
                circle_point
            ])

        # 브레이스 표시 여부에 따라 처리
        self._update_brace_config(alpha, x, y, circle_point, x_intercept)

    def _update_brace_config(self, alpha, x, y, circle_point, x_intercept):
        self.brace_config = None

        # sec 값이 너무 크지 않을 때만 브레이스 표시
        show_brace_for_frame = alpha > 0 and abs(1 / x) < 5

        if not show_brace_for_frame:
            return

        # 빗변의 방향 벡터 계산
        origin = self.base_unit_circle.plane.c2p(0, 0)  # 원점의 실제 좌표
        direction_vector = np.array(x_intercept) - np.array(origin)
        direction_length = np.linalg.norm(direction_vector)

        if direction_length == 0:
            return

        normalized_direction = direction_vector / direction_length
        # 브레이스 방향을 수직으로 설정 (반대 방향)
        brace_direction = - \
            np.array([-normalized_direction[1], normalized_direction[0], 0])

        # y 좌표가 음수일 때 방향 반전
        if y < 0:
            brace_direction = -brace_direction

        # 2,3사분면(x < 0)에서 방향 반전
        if x < 0:
            brace_direction = -brace_direction

        self.brace_config = BraceConfig(
            ref_obj=self.base_unit_circle.secant_line,
            direction=brace_direction,
            text="\\sec(x)",
            buff=self.base_unit_circle.base_buff * 0.5
        )
