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
