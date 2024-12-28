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
        self.base_unit_circle.remove_brace_by_trig_name(trig_name)

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
