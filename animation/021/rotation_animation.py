from typing import override, final, abstractmethod
from dataclasses import dataclass
from manim import *
from base_unit_circle import BaseUnitCircle, ZIndexEnum, StyleConfig


@dataclass
class BraceConfig:
    ref_obj: Mobject
    direction: np.ndarray | str
    text: str
    buff: float = None


class BaseRotation(Animation):
    """단위원에서 삼각함수 회전을 시각화하는 애니메이션의 베이스 클래스"""

    base_unit_circle: BaseUnitCircle
    clockwise: bool
    rotation_count: int
    show_brace: bool
    remove_shapes: bool

    brace_config: BraceConfig = None

    def __init__(
        self,
        base_unit_circle: BaseUnitCircle,
        clockwise: bool = False,
        rotation_count: int = 1,
        show_brace: bool = True,
        remove_shapes: bool = True,
        **kwargs
    ):
        super().__init__(base_unit_circle, **kwargs)
        self.base_unit_circle = base_unit_circle
        self.clockwise = clockwise
        self.rotation_count = rotation_count
        self.show_brace = show_brace
        self.remove_shapes = remove_shapes

    @final
    @override
    def begin(self):
        self.before_begin()
        return super().begin()

    @final
    @override
    def finish(self):
        retVal = super().finish()
        self.after_finish()
        self.brace_config = None
        return retVal

    @final
    @override
    def interpolate_mobject(self, alpha):
        # 현재 회전 각도 계산
        current_angle = self.calculate_current_angle_from(alpha)

        # 메인 객체들 업데이트
        self.update_main_objects_state(alpha, current_angle)

        # 부수적인 객체들 업데이트
        self.update_side_objects_state(alpha, current_angle)

    @abstractmethod
    def trig_name(self) -> str:
        """삼각함수 이름을 반환"""
        pass

    @abstractmethod
    def before_begin(self) -> None:
        """애니메이션 시작 전 필요한 준비 작업을 수행"""
        pass

    @abstractmethod
    def after_finish(self) -> None:
        """애니메이션 종료 후 필요한 작업을 수행"""
        pass

    @abstractmethod
    def update_main_objects_state(self, alpha: float, current_angle: float) -> None:
        """메인 객체들의 애니메이션 중간 상태를 업데이트"""
        pass

    def update_side_objects_state(self, alpha: float, current_angle: float) -> None:
        """부수적인 객체들의 애니메이션 중간 상태를 업데이트"""

        trig_name = self.trig_name()

        # 기존 브레이스 제거
        self.remove_brace_and_label(trig_name)

        if self.show_brace and self.brace_config:
            self.add_brace_and_label(
                self.brace_config.ref_obj,
                self.brace_config.direction,
                f"{trig_name}_brace",
                self.brace_config.text,
                buff=self.brace_config.buff,
                store_key=trig_name
            )

    @final
    def calculate_current_angle_from(self, progress_alpha: float) -> float:
        """회전 각도를 계산하는 공통 메서드"""
        alpha = progress_alpha
        total_rotation = TAU * self.rotation_count
        if self.clockwise:
            total_rotation = -total_rotation
        return self.base_unit_circle.initial_angle + (alpha * total_rotation)

    @final
    def add_brace_and_label(
        self,
        target_mobject: Mobject,
        direction: np.ndarray | str,
        name: str,
        text: str,
        buff: float = None,
        store_key: str = None  # decorations 딕셔너리의 키값
    ) -> tuple[Mobject, Mobject]:
        """브레이스와 라벨을 추가하는 공통 메서드"""
        brace, label = self.base_unit_circle.plane_group.add_brace(
            target_mobject,
            direction=direction,
            name=name,
            text=text,
            color=StyleConfig.BRACE_COLOR,
            text_color=StyleConfig.BRACE_TEXT_COLOR,
            buff=buff or self.base_unit_circle.base_buff,
            text_buff=self.base_unit_circle.adjusted_text_buff,
            font_size=self.base_unit_circle.adjusted_font_size
        )

        # z_index 설정
        brace.set_z_index(ZIndexEnum.DECORATIONS)
        label.set_z_index(ZIndexEnum.DECORATIONS)

        # VGroup에 추가하기 전에 기존 객체들의 z_index 확인
        for mob in self.base_unit_circle.submobjects:
            if not hasattr(mob, 'z_index'):
                mob.set_z_index(ZIndexEnum.BACKGROUND)

        # VGroup에도 추가
        self.base_unit_circle.add(brace, label)

        # decorations 딕셔너리에 저장
        if store_key:
            self.base_unit_circle.decorations[store_key] = (brace, label)

        return brace, label

    @final
    def remove_brace_and_label(self, key: str) -> None:
        """브레이스와 라벨을 제거하는 공통 메서드"""
        if key in self.base_unit_circle.decorations:
            brace, label = self.base_unit_circle.decorations[key]
            if brace is not None:
                self.base_unit_circle.remove(brace, label)
                self.base_unit_circle.plane_group.remove_brace(f"{key}_brace")
            self.base_unit_circle.decorations.pop(key)


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
        if self.base_unit_circle.point_of_tangency:
            self.base_unit_circle\
                .point_of_tangency\
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

        if self.base_unit_circle.circle_radius:
            self.base_unit_circle\
                .circle_radius\
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

        if self.base_unit_circle.hypotenuse:
            self.base_unit_circle\
                .hypotenuse\
                .set_points_by_ends(circle_point, x_intercept)

        if self.base_unit_circle.inner_triangle:
            self.base_unit_circle.inner_triangle\
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
            ref_obj=self.base_unit_circle.hypotenuse,
            direction=brace_direction,
            text="\\tan(x)",
            buff=self.base_unit_circle.base_buff * 0.5
        )
