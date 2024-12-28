from typing import override
from manim import *
from base_rotation import BaseRotation, BraceConfig


class SineRotation(BaseRotation):
    """단위원에서 '싸인 활꼴 회전'을 시각화하는 애니메이션"""

    @override
    def trig_name(self) -> str:
        return "sine"

    @override
    def before_begin(self):
        self.base_unit_circle.add_shapes_for_sine()

    @override
    def after_finish(self):
        if self.remove_shapes:
            self.base_unit_circle.remove_shapes_for_sine()

    @override
    def update_main_objects_state(self, alpha, current_angle):
        plane = self.base_unit_circle.plane

        # 현재 시점 회전각 위치에서의 단위원 상을 이동하는 점의 좌표 계산
        x = np.cos(current_angle)
        y = np.sin(current_angle)

        # 평면 좌표로 변환
        origin = plane.c2p(0, 0)
        circle_point = plane.c2p(x, y)
        x_point = plane.c2p(x, 0)

        # 삼각형 업데이트
        triangle_points = [origin, circle_point, x_point, origin]
        lower_points = [
            origin,
            plane.c2p(x, -y),
            x_point,
            origin
        ]  # 하단 삼각형은 y 좌표만 반전

        # 상단 삼각형
        self.base_unit_circle\
            .upper_triangle\
            .set_points_as_corners(triangle_points)

        # 하단 삼각형
        self.base_unit_circle\
            .lower_triangle\
            .set_points_as_corners(lower_points)

        # '피처 현' 업데이트
        self.base_unit_circle\
            .upper_half_chord\
            .set_points_by_ends(circle_point, x_point)
        self.base_unit_circle\
            .lower_half_chord\
            .set_points_by_ends(plane.c2p(x, -y), x_point)

        # 점 업데이트
        self.base_unit_circle.upper_dot.move_to(circle_point)
        self.base_unit_circle.lower_dot.move_to(plane.c2p(x, -y))

        # 브레이스 표시 여부에 따라 처리
        self._update_brace_config(alpha, x, y)

    def _update_brace_config(self, alpha, x, y):
        self.brace_config = None

        # 현재 좌표계의 스케일을 고려한 최소 높이 계산
        unit_y_height = abs(
            self.base_unit_circle.plane.c2p(0, 1)[1]
            - self.base_unit_circle.plane.c2p(0, 0)[1]
        )

        circle_point_height = abs(y)
        min_height = 0.1 * unit_y_height

        # 브레이스 표시 여부 플래그 설정:
        # - 첫번째 프레임에서는 브레이스를 표시하지 않음
        # - 'sin 값(=현의 높이)'이 너무 작을 때도 브레이스를 표시하지 않음
        show_brace_for_frame = alpha > 0 and circle_point_height > min_height

        if show_brace_for_frame:
            self.brace_config = BraceConfig(
                ref_obj=self.base_unit_circle.upper_half_chord,
                direction=RIGHT if x >= 0 else LEFT,
                text="\\sin(x)"
            )


class CosecantRotation(BaseRotation):
    """단위원에서 '코시컨트 회전'을 시각화하는 애니메이션"""

    @override
    def trig_name(self) -> str:
        return "cosecant"

    @override
    def before_begin(self):
        self.base_unit_circle.add_shapes_for_cosecant()

    @override
    def after_finish(self):
        if self.remove_shapes:
            self.base_unit_circle.remove_shapes_for_cosecant()

    @override
    def update_main_objects_state(self, alpha, current_angle):
        plane = self.base_unit_circle.plane

        # 1. 단위원 상의 점 계산
        x = np.cos(current_angle)
        y = np.sin(current_angle)

        circle_point = plane.c2p(x, y)

        # 2. y축 투영점 계산
        y_projection = plane.c2p(0, y)

        # 3. 불연속점 체크 (0° 또는 180° 근처)
        EPSILON = 1e-3
        is_near_discontinuity = abs(current_angle % PI) < EPSILON

        if is_near_discontinuity or abs(y) <= EPSILON:
            return

        # 4. y축과의 교점 계산 (csc = 1/sin)
        csc_y = 1 / y
        y_intercept = plane.c2p(0, csc_y)

        # 모든 요소 기존 상태 유지하며 업데이트
        if self.base_unit_circle.cosecant_point:
            self.base_unit_circle.cosecant_point.move_to(circle_point)

        if self.base_unit_circle.cosecant_y_projection:
            self.base_unit_circle.cosecant_y_projection.move_to(y_projection)

        if self.base_unit_circle.cosecant_y_axis_intercept:
            self.base_unit_circle\
                .cosecant_y_axis_intercept\
                .set_opacity(1)\
                .move_to(y_intercept)

        if self.base_unit_circle.cosecant_radius:
            self.base_unit_circle.cosecant_radius.set_points_by_ends(
                plane.c2p(0, 0), circle_point
            )

        if self.base_unit_circle.cosecant_line:
            self.base_unit_circle.cosecant_line.set_points_by_ends(
                plane.c2p(0, 0), y_intercept
            )

        if self.base_unit_circle.cosecant_inner_triangle:
            self.base_unit_circle.cosecant_inner_triangle.set_points_as_corners([
                plane.c2p(0, 0),
                circle_point,
                y_projection,
                plane.c2p(0, 0)
            ])

        if self.base_unit_circle.cosecant_outer_triangle:
            self.base_unit_circle.cosecant_outer_triangle.set_points_as_corners([
                circle_point,
                y_projection,
                y_intercept,
                circle_point
            ])

        # 브레이스 표시 여부에 따라 처리
        self._update_brace_config(alpha, x, y, circle_point, y_intercept)

    def _update_brace_config(self, alpha, x, y, circle_point, y_intercept):
        self.brace_config = None

        # csc 값이 너무 크지 않을 때만 브레이스 표시
        show_brace_for_frame = alpha > 0 and abs(1 / y) < 5

        if not show_brace_for_frame:
            return

        # 빗변의 방향 벡터 계산
        origin = self.base_unit_circle.plane.c2p(0, 0)  # 원점의 실제 좌표
        direction_vector = np.array(y_intercept) - np.array(origin)
        direction_length = np.linalg.norm(direction_vector)

        if direction_length == 0:
            return

        normalized_direction = direction_vector / direction_length
        # 브레이스 방향을 수직으로 설정
        brace_direction = np.array(
            [-normalized_direction[1], normalized_direction[0], 0])

        # x 좌표가 음수일 때 방향 반전
        if x < 0:
            brace_direction = -brace_direction

        # 3,4분면(y < 0)에서 방향 반전
        if y < 0:
            brace_direction = -brace_direction

        self.brace_config = BraceConfig(
            ref_obj=self.base_unit_circle.cosecant_line,
            direction=brace_direction,
            text="\\csc(x)",
            buff=self.base_unit_circle.base_buff * 0.5
        )
