from typing import override
from manim import *
from base_unit_circle import BaseUnitCircle


class SineRotation(Animation):
    """단위원에서 '싸인 활꼴 회전'을 시각화하는 애니메이션"""

    clockwise: bool
    unit_circle_triangle: BaseUnitCircle
    rotation_count: int
    show_brace: bool
    remove_shapes: bool

    def __init__(
        self,
        unit_circle_triangle: BaseUnitCircle,
        clockwise: bool = False,
        rotation_count: int = 1,
        show_brace: bool = True,
        remove_shapes: bool = True,
        **kwargs
    ):
        super().__init__(unit_circle_triangle, **kwargs)
        self.clockwise = clockwise
        self.unit_circle_triangle = unit_circle_triangle
        self.rotation_count = rotation_count  # 회전 횟수 추가
        self.show_brace = show_brace  # 브레이스 표시 여부
        self.remove_shapes = remove_shapes  # 애니메이션 종료 시 도형 제거 여부

    @override
    def begin(self):
        self.unit_circle_triangle.add_shapes_for_sine()
        return super().begin()

    @override
    def finish(self):
        retVal = super().finish()
        if self.remove_shapes:
            self.unit_circle_triangle.remove_shapes_for_sine()
        return retVal

    @override
    def interpolate_mobject(self, alpha):
        # 첫 프레임에서는 브레이스를 표시하지 않음
        show_brace_for_frame = self.show_brace and alpha > 0

        # initial_angle부터 시작하여 회전
        angle = self.unit_circle_triangle.initial_angle + \
            (alpha * TAU * self.rotation_count)
        if self.clockwise:
            angle = self.unit_circle_triangle.initial_angle - \
                (alpha * TAU * self.rotation_count)

        x = np.cos(angle)
        y = np.sin(angle)

        # 평면 좌표로 변환
        plane = self.unit_circle_triangle.plane
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
        self.unit_circle_triangle.upper_triangle.set_points_as_corners(
            triangle_points)

        # 하단 삼각형 (flip 불필요)
        self.unit_circle_triangle.lower_triangle.set_points_as_corners(
            lower_points)

        # 현 업데이트
        self.unit_circle_triangle.upper_half_chord.set_points_by_ends(
            circle_point, x_point)
        self.unit_circle_triangle.lower_half_chord.set_points_by_ends(
            plane.c2p(x, -y), x_point)

        # 현의 높이(sin 값)가 일정 크기 이상일 때만 브레이스 표시
        height = abs(y)

        # 현재 좌표계의 스케일을 고려한 최소 높이 계산
        unit_y = abs(self.unit_circle_triangle.plane.c2p(0, 1)[1] -
                     self.unit_circle_triangle.plane.c2p(0, 0)[1])
        min_height = 0.1 * unit_y

        # 기존 브레이스 제거
        if "sine" in self.unit_circle_triangle.decorations:
            brace, label = self.unit_circle_triangle.decorations["sine"]
            if brace is not None:
                self.unit_circle_triangle.remove(brace, label)
                self.unit_circle_triangle.plane_group.remove_brace(
                    "sine_brace")
            self.unit_circle_triangle.decorations.pop("sine")

        # 브레이스 표시 여부에 따라 처리
        if show_brace_for_frame and height > min_height:
            # x 값에 따라 브레이스가 붙을 현의 방향 결정
            brace_direction = RIGHT  # 1, 4분면 (x >= 0)
            if x < 0:  # 2, 3분면
                brace_direction = LEFT

            # 미리 계산된 폰트 크기 사용
            brace, label = self.unit_circle_triangle.plane_group.add_brace(
                self.unit_circle_triangle.upper_half_chord,
                direction=brace_direction,
                name="sine_brace",
                text="\\sin(x)",
                color=YELLOW,
                text_color=YELLOW,
                buff=self.unit_circle_triangle.base_buff,  # 기본 버퍼 사용
                text_buff=self.unit_circle_triangle.adjusted_text_buff,  # 조정된 버퍼 사용
                font_size=self.unit_circle_triangle.adjusted_font_size
            )

            # z_index 설정으로 항상 위에 표시
            brace.set_z_index(2)
            label.set_z_index(2)

            # VGroup에 추가하기 전에 기존 객체들의 z_index 확인
            for mob in self.unit_circle_triangle.submobjects:
                if not hasattr(mob, 'z_index'):
                    mob.set_z_index(0)

            # VGroup에도 추가
            self.unit_circle_triangle.add(brace, label)
            self.unit_circle_triangle.decorations["sine"] = (brace, label)

        # 점 업데이트
        self.unit_circle_triangle.upper_dot.move_to(circle_point)
        self.unit_circle_triangle.lower_dot.move_to(plane.c2p(x, -y))


class CosineRotation(Animation):
    """단위원에서 '코싸인 활꼴 회전'을 시각화하는 애니메이션"""

    clockwise: bool
    unit_circle_triangle: BaseUnitCircle
    rotation_count: int
    show_brace: bool
    remove_shapes: bool

    def __init__(
        self,
        unit_circle_triangle: BaseUnitCircle,
        clockwise: bool = False,
        rotation_count: int = 1,
        show_brace: bool = True,
        remove_shapes: bool = True,
        **kwargs
    ):
        super().__init__(unit_circle_triangle, **kwargs)
        self.clockwise = clockwise
        self.unit_circle_triangle = unit_circle_triangle
        self.rotation_count = rotation_count
        self.show_brace = show_brace
        self.remove_shapes = remove_shapes

    @override
    def begin(self):
        self.unit_circle_triangle.add_shapes_for_cosine()
        return super().begin()

    @override
    def finish(self):
        retVal = super().finish()
        if self.remove_shapes:
            self.unit_circle_triangle.remove_shapes_for_cosine()
        return retVal

    @override
    def interpolate_mobject(self, alpha):
        # 첫 프레임에서는 브레이스를 표시하지 않음
        show_brace_for_frame = self.show_brace and alpha > 0

        # 회전 각도 계산 방식 수정
        total_rotation = TAU * self.rotation_count
        if self.clockwise:
            total_rotation = -total_rotation

        # initial_angle을 시작점으로, 거기서부터 total_rotation만큼 회전
        angle = self.unit_circle_triangle.initial_angle + \
            (alpha * total_rotation)

        x = np.cos(angle)
        y = np.sin(angle)

        # 평면 좌표로 변환
        plane = self.unit_circle_triangle.plane
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
        self.unit_circle_triangle.right_triangle.set_points_as_corners(
            triangle_points)

        # 좌측 삼각형
        self.unit_circle_triangle.left_triangle.set_points_as_corners(
            left_points)

        # 현 업데이트
        self.unit_circle_triangle.right_half_chord.set_points_by_ends(
            circle_point, y_point)
        self.unit_circle_triangle.left_half_chord.set_points_by_ends(
            plane.c2p(-x, y), y_point)

        # 현의 너비(cos 값)가 일정 크기 이상일 때만 브레이스 표시
        width = abs(x)

        # 현재 좌표계의 스케일을 고려한 최소 너비 계산
        unit_x = abs(self.unit_circle_triangle.plane.c2p(1, 0)[0] -
                     self.unit_circle_triangle.plane.c2p(0, 0)[0])
        min_width = 0.1 * unit_x

        # 기존 브레이스 제거
        if "cosine" in self.unit_circle_triangle.decorations:
            brace, label = self.unit_circle_triangle.decorations["cosine"]
            if brace is not None:
                self.unit_circle_triangle.remove(brace, label)
                self.unit_circle_triangle.plane_group.remove_brace(
                    "cosine_brace")
            self.unit_circle_triangle.decorations.pop("cosine")

        # 브레이스 표시 여부에 따라 처리
        if show_brace_for_frame and width > min_width:
            # y 값에 따라 브레이스가 붙을 현의 방향 결정
            brace_direction = UP  # 1, 2분면 (y >= 0)
            if y < 0:  # 3, 4분면
                brace_direction = DOWN

            # 미리 계산된 폰트 크기 사용
            brace, label = self.unit_circle_triangle.plane_group.add_brace(
                self.unit_circle_triangle.right_half_chord,
                direction=brace_direction,
                name="cosine_brace",
                text="\\cos(x)",
                color=YELLOW,
                text_color=YELLOW,
                buff=self.unit_circle_triangle.base_buff,  # 기본 버퍼 사용
                text_buff=self.unit_circle_triangle.adjusted_text_buff,  # 조정된 버퍼 사용
                font_size=self.unit_circle_triangle.adjusted_font_size
            )

            # z_index 설정
            brace.set_z_index(2)
            label.set_z_index(2)

            # VGroup에 추가하기 전에 기존 객체들의 z_index 확인
            for mob in self.unit_circle_triangle.submobjects:
                if not hasattr(mob, 'z_index'):
                    mob.set_z_index(0)

            # VGroup에도 추가
            self.unit_circle_triangle.add(brace, label)
            self.unit_circle_triangle.decorations["cosine"] = (brace, label)

        # 점 업데이트
        self.unit_circle_triangle.right_dot.move_to(circle_point)
        self.unit_circle_triangle.left_dot.move_to(plane.c2p(-x, y))


class TangentRotation(Animation):
    """단위원에서 '탄젠트 회전'을 시각화하는 애니메이션"""

    clockwise: bool
    unit_circle_triangle: BaseUnitCircle
    rotation_count: int
    show_brace: bool
    remove_shapes: bool

    def __init__(
        self,
        unit_circle_triangle: BaseUnitCircle,
        clockwise: bool = False,
        rotation_count: int = 1,
        show_brace: bool = True,
        remove_shapes: bool = True,
        **kwargs
    ):
        super().__init__(unit_circle_triangle, **kwargs)
        self.clockwise = clockwise
        self.unit_circle_triangle = unit_circle_triangle
        self.rotation_count = rotation_count
        self.show_brace = show_brace
        self.remove_shapes = remove_shapes

    @override
    def begin(self):
        # 시작할 때 이전의 브레이스/라벨이 있다면 제거
        if "tangent" in self.unit_circle_triangle.decorations:
            brace, label = self.unit_circle_triangle.decorations["tangent"]
            if brace is not None:
                self.unit_circle_triangle.remove(brace, label)
                self.unit_circle_triangle.plane_group.remove_brace(
                    "tangent_brace")
            self.unit_circle_triangle.decorations.pop("tangent")
        self.unit_circle_triangle.add_shapes_for_tangent()
        return super().begin()

    @override
    def finish(self):
        retVal = super().finish()
        if self.remove_shapes:
            self.unit_circle_triangle.remove_shapes_for_tangent()
        return retVal

    @override
    def interpolate_mobject(self, alpha):
        # 매 프레임마다 이전 브레이스/라벨 제거 확실히 하기
        if hasattr(self, 'current_brace'):
            self.unit_circle_triangle.remove(
                self.current_brace, self.current_label)
            self.current_brace = None
            self.current_label = None

        # 회전 각도 계산
        angle = self.unit_circle_triangle.initial_angle + \
            (alpha * TAU * self.rotation_count)
        if self.clockwise:
            angle = self.unit_circle_triangle.initial_angle - \
                (alpha * TAU * self.rotation_count)

        # 현재 좌표계
        plane = self.unit_circle_triangle.plane

        # 1. 단위원 위의 점 업데이트
        x = np.cos(angle)
        y = np.sin(angle)
        circle_point = plane.c2p(x, y)
        # 기존에 생성된 점 이동
        if self.unit_circle_triangle.point_of_tangency:
            self.unit_circle_triangle.point_of_tangency.move_to(circle_point)

        # 2. x축 투영점 계산
        x_projection = plane.c2p(x, 0)

        # 3. 불연속점 체크 (90° 또는 270° 근처)
        EPSILON = 1e-3
        is_near_discontinuity = abs(abs(angle % PI) - PI/2) < EPSILON

        # 항상 기존 브레이스 제거 (불연속점 여부와 관계없이)
        if "tangent" in self.unit_circle_triangle.decorations:
            brace, label = self.unit_circle_triangle.decorations["tangent"]
            if brace is not None:
                self.unit_circle_triangle.remove(brace, label)
                self.unit_circle_triangle.plane_group.remove_brace(
                    "tangent_brace")
            self.unit_circle_triangle.decorations.pop("tangent")

        if not is_near_discontinuity:
            # 4. x축과의 교점 계산
            if abs(x) > EPSILON:  # cos(θ) ≠ 0
                sec_x = 1/x  # secant = 1/cos
                x_intercept = plane.c2p(sec_x, 0)

                # 모든 요소 기존 상태 유지하며 업데이트
                if self.unit_circle_triangle.x_axis_intercept:
                    self.unit_circle_triangle.x_axis_intercept.move_to(
                        x_intercept)

                if self.unit_circle_triangle.circle_radius:
                    self.unit_circle_triangle.circle_radius.set_points_by_ends(
                        plane.c2p(0, 0), circle_point
                    )

                if self.unit_circle_triangle.hypotenuse:
                    self.unit_circle_triangle.hypotenuse.set_points_by_ends(
                        circle_point, x_intercept
                    )

                if self.unit_circle_triangle.inner_triangle:
                    self.unit_circle_triangle.inner_triangle\
                        .set_points_as_corners([
                            plane.c2p(0, 0),
                            circle_point,
                            x_projection,
                            plane.c2p(0, 0)
                        ])

                if self.unit_circle_triangle.tangent_triangle:
                    self.unit_circle_triangle.tangent_triangle\
                        .set_points_as_corners([
                            circle_point,
                            x_intercept,
                            x_projection,
                            circle_point
                        ])

                # 불연속점이 아닐 때는 원래의 opacity로 복원
                for mob in [self.unit_circle_triangle.x_axis_intercept,
                            self.unit_circle_triangle.hypotenuse,
                            self.unit_circle_triangle.tangent_triangle]:
                    if mob and hasattr(mob, '_default_opacity'):
                        mob.set_opacity(mob._default_opacity)

                # tan 값이 너무 크지 않을 때만 브레이스 표시
                if abs(y/x) < 5 and self.show_brace and alpha > 0:
                    # 빗변의 방향 벡터 계산
                    start_point = np.array(circle_point)
                    end_point = np.array(x_intercept)
                    direction_vector = end_point - start_point
                    direction_length = np.linalg.norm(direction_vector)

                    if direction_length == 0:
                        # 방향 벡터가 0이면 다음 단계 건너뛰기
                        return

                    normalized_direction = direction_vector / direction_length

                    brace_direction = np.array(
                        [-normalized_direction[1], normalized_direction[0], 0])

                    if x < 0:
                        brace_direction = -brace_direction

                    # 3, 4분면에서 바깥쪽으로 향하게 반전
                    if y < 0:
                        brace_direction = -brace_direction

                    # 브레이스와 텍스트 추가
                    brace, label = self.unit_circle_triangle.plane_group.add_brace(
                        self.unit_circle_triangle.hypotenuse,
                        direction=brace_direction,  # 계산된 방향 벡터 사용
                        name="tangent_brace",
                        text="\\tan(x)",
                        color=YELLOW,
                        text_color=YELLOW,
                        buff=self.unit_circle_triangle.base_buff * 0.5,  # 버퍼 크기 조정
                        text_buff=self.unit_circle_triangle.adjusted_text_buff,
                        font_size=self.unit_circle_triangle.adjusted_font_size
                    )

                    # 현재 프레임의 브레이스/라벨 저장
                    self.current_brace = brace
                    self.current_label = label

                    # z_index 설정으로 항상 위에 표시
                    brace.set_z_index(4)
                    label.set_z_index(4)

                    # VGroup에 추가
                    self.unit_circle_triangle.add(brace, label)
                    self.unit_circle_triangle.decorations["tangent"] = (
                        brace, label)
