from typing import override
from manim import *
from base_rotation import BaseRotation, BraceConfig


class TangentRotation(BaseRotation):
    """단위원에서 '탄젠트 회전'을 시각화하는 애니메이션"""

    @override
    def trig_name(self) -> str:
        return "tangent"

    @override
    def before_begin(self):
        self.base_unit_circle.add_shapes_for_tangent()

    @override
    def after_finish(self):
        if self.remove_shapes:
            self.base_unit_circle.remove_shapes_for_tangent()

    @override
    def update_main_objects_state(self, alpha, current_angle):
        plane = self.base_unit_circle.plane

        # 1. 단위원 상의 점 계산
        x = np.cos(current_angle)
        y = np.sin(current_angle)

        circle_point = plane.c2p(x, y)

        # 기존에 생성된 점 이동
        if self.base_unit_circle.tangent_point:
            self.base_unit_circle\
                .tangent_point\
                .move_to(circle_point)

        # 2. x축 투영점 계산
        x_projection = plane.c2p(x, 0)

        # 3. 불연속점 체크 (90° 또는 270° 근처)
        EPSILON = 1e-3
        is_near_discontinuity = abs(abs(current_angle % PI) - PI/2) < EPSILON

        if is_near_discontinuity or abs(x) <= EPSILON:
            return

        # 4. x축과의 교점 계산
        sec_x = 1 / x  # secant = 1/cos
        x_intercept = plane.c2p(sec_x, 0)

        # 모든 요소 기존 상태 유지하며 업데이트
        if self.base_unit_circle.x_axis_intercept:
            self.base_unit_circle\
                .x_axis_intercept\
                .move_to(x_intercept)

        if self.base_unit_circle.tangent_radius:
            self.base_unit_circle\
                .tangent_radius\
                .set_points_by_ends(plane.c2p(0, 0), circle_point)

        if self.base_unit_circle.tangent_line:
            # 평면 좌표로 변환하여 3D 벡터로 만듦
            _, start_point, end_point = self.base_unit_circle\
                                            .calculate_tangent_line_points(current_angle)
            start_pt = self.base_unit_circle.plane.c2p(*start_point)
            end_pt = self.base_unit_circle.plane.c2p(*end_point)
            self.base_unit_circle\
                .tangent_line\
                .set_points_by_ends(start_pt, end_pt)

        if self.base_unit_circle.tangent_hypotenuse:
            self.base_unit_circle\
                .tangent_hypotenuse\
                .set_points_by_ends(circle_point, x_intercept)

        if self.base_unit_circle.tangent_inner_triangle:
            self.base_unit_circle.tangent_inner_triangle\
                .set_points_as_corners([
                    plane.c2p(0, 0),
                    circle_point,
                    x_projection,
                    plane.c2p(0, 0)
                ])

        if self.base_unit_circle.tangent_triangle:
            self.base_unit_circle.tangent_triangle\
                .set_points_as_corners([
                    circle_point,
                    x_intercept,
                    x_projection,
                    circle_point
                ])

        # 브레이스 표시 여부에 따라 처리
        self._update_brace_config(
            alpha, x, y, circle_point, x_intercept
        )

    def _update_brace_config(self, alpha, x, y, circle_point, x_intercept):
        self.brace_config = None

        # tan 값이 너무 크지 않을 때만 브레이스 표시
        show_brace_for_frame = alpha > 0 and abs(y / x) < 5

        if not show_brace_for_frame:
            return

        # 빗변의 방향 벡터 계산
        start_pt = np.array(circle_point)
        end_pt = np.array(x_intercept)
        direction_vector = end_pt - start_pt
        direction_length = np.linalg.norm(direction_vector)

        if direction_length == 0:
            return

        normalized_direction = direction_vector / direction_length
        brace_direction = np.array(
            [-normalized_direction[1], normalized_direction[0], 0]
        )

        if x < 0:
            brace_direction = -brace_direction

        # 3, 4분면에서 바깥쪽으로 향하게 반전
        if y < 0:
            brace_direction = -brace_direction

        self.brace_config = BraceConfig(
            ref_obj=self.base_unit_circle.tangent_hypotenuse,
            direction=brace_direction,
            text="\\tan(x)",
            buff=self.base_unit_circle.base_buff * 0.5
        )


class CotangentRotation(BaseRotation):
    """단위원에서 '코탄젠트 회전'을 시각화하는 애니메이션"""

    @override
    def trig_name(self) -> str:
        return "cotangent"

    @override
    def before_begin(self):
        self.base_unit_circle.add_shapes_for_cotangent()

    @override
    def after_finish(self):
        if self.remove_shapes:
            self.base_unit_circle.remove_shapes_for_cotangent()

    @override
    def update_main_objects_state(self, alpha, current_angle):
        plane = self.base_unit_circle.plane

        # 1. 단위원 상의 점 계산
        x = np.cos(current_angle)
        y = np.sin(current_angle)

        circle_point = plane.c2p(x, y)

        # 기존에 생성된 점 이동
        if self.base_unit_circle.cotangent_point:
            self.base_unit_circle\
                .cotangent_point\
                .move_to(circle_point)

        # 2. y축 투영점 계산
        y_projection = plane.c2p(0, y)

        # 3. 불연속점 체크 (0° 또는 180° 근처)
        EPSILON = 1e-3
        is_near_discontinuity = abs(current_angle % PI) < EPSILON

        if is_near_discontinuity or abs(y) <= EPSILON:
            return

        # 4. y축과의 교점 계산
        csc_y = 1 / y  # cosecant = 1/sin
        y_intercept = plane.c2p(0, csc_y)

        # 모든 요소 기존 상태 유지하며 업데이트
        if self.base_unit_circle.y_axis_intercept:
            self.base_unit_circle\
                .y_axis_intercept\
                .move_to(y_intercept)

        if self.base_unit_circle.cotangent_radius:
            self.base_unit_circle\
                .cotangent_radius\
                .set_points_by_ends(plane.c2p(0, 0), circle_point)

        if self.base_unit_circle.cotangent_line:
            # 평면 좌표로 변환하여 3D 벡터로 만듦
            _, start_point, end_point\
                = self.base_unit_circle.calculate_tangent_line_points(current_angle)
            start_pt = self.base_unit_circle.plane.c2p(*start_point)
            end_pt = self.base_unit_circle.plane.c2p(*end_point)
            self.base_unit_circle\
                .cotangent_line\
                .set_points_by_ends(start_pt, end_pt)

        if self.base_unit_circle.cotangent_hypotenuse:
            self.base_unit_circle\
                .cotangent_hypotenuse\
                .set_points_by_ends(circle_point, y_intercept)

        if self.base_unit_circle.cotangent_inner_triangle:
            self.base_unit_circle.cotangent_inner_triangle\
                .set_points_as_corners([
                    plane.c2p(0, 0),
                    circle_point,
                    y_projection,
                    plane.c2p(0, 0)
                ])

        if self.base_unit_circle.cotangent_triangle:
            self.base_unit_circle.cotangent_triangle\
                .set_points_as_corners([
                    circle_point,
                    y_intercept,
                    y_projection,
                    circle_point
                ])

        # 브레이스 표시 여부에 따라 처리
        self._update_brace_config(
            alpha, x, y, circle_point, y_intercept
        )

    def _update_brace_config(self, alpha, x, y, circle_point, y_intercept):
        self.brace_config = None

        # cot 값이 너무 크지 않을 때만 브레이스 표시
        show_brace_for_frame = alpha > 0 and abs(x / y) < 5

        if not show_brace_for_frame:
            return

        # 빗변의 방향 벡터 계산
        start_pt = np.array(circle_point)
        end_pt = np.array(y_intercept)
        direction_vector = end_pt - start_pt
        direction_length = np.linalg.norm(direction_vector)

        if direction_length == 0:
            return

        normalized_direction = direction_vector / direction_length
        # 브레이스 방향을 반대로 설정 (tangent와 반대)
        brace_direction = -np.array(
            [-normalized_direction[1], normalized_direction[0], 0]
        )

        if y < 0:
            brace_direction = -brace_direction

        # 2, 3분면에서 바깥쪽으로 향하게 반전
        if x < 0:
            brace_direction = -brace_direction

        self.brace_config = BraceConfig(
            ref_obj=self.base_unit_circle.cotangent_hypotenuse,
            direction=brace_direction,
            text="\\cot(x)",
            buff=self.base_unit_circle.base_buff * 0.5
        )
