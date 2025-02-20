from typing import Tuple, Optional, List
import numpy as np
from manim import *
from common.logic_gate.logic_gate import LogicGate
from common.logic_gate.not_gate import NotGate
from common.logic_gate.and_gate import AndGate
from common.logic_gate.or_gate import OrGate
from common.logic_gate.nand_gate import NandGate
from common.logic_gate.nor_gate import NorGate
from common.logic_gate.xor_gate import XorGate
from common.logic_gate.wire import Wire
from common.logic_gate.styles import LogicGateStyle


class BreadBoardPlane(NumberPlane):
    # 스타일 상수 정의
    AXIS_STYLE = {
        "color": GREY_C,
        "stroke_opacity": 0.3
    }
    GRID_STYLE = {
        "stroke_color": GREY_B,
        "stroke_width": 1,
        "stroke_opacity": 0.3
    }

    def __init__(self, **kwargs):
        super().__init__(
            axis_config=self.AXIS_STYLE,
            x_axis_config=self.AXIS_STYLE,
            y_axis_config=self.AXIS_STYLE,
            background_line_style=self.GRID_STYLE,
            **kwargs
        )
        self.scale_factor = 1
        self.shift_vector = ORIGIN

    # shift를 오버라이드하여 shift_vector 기록
    def shift(self, vector, **kwargs):
        result = super().shift(vector, **kwargs)
        self.shift_vector = getattr(self, "shift_vector", ORIGIN) + vector
        return result

    # 스케일 적용 시 scale_factor 저장
    def scale(self, factor, **kwargs):
        self.scale_factor = factor
        return super().scale(factor, **kwargs)

    def _create_gate_common(self,
                            pos: tuple[float, float] | tuple[float, float, float],
                            gate_class: type,
                            **kwargs) -> LogicGate:
        """기본 논리 게이트 생성을 위한 공통 메서드"""
        scaled_size = kwargs.get(
            'size', LogicGateStyle.DEFAULT_SIZE) * self.scale_factor
        kwargs['size'] = scaled_size

        screen_pos = self.c2p(*pos) if len(pos) == 3 else self.c2p(
            pos[0], pos[1], LogicGateStyle.DEFAULT_Z_COORD)

        gate = gate_class(**kwargs).move_to(screen_pos)
        self.add(gate)
        return gate

    # 기본 게이트 생성 메서드들만 유지
    def create_not_gate(self, pos, **kwargs) -> NotGate:
        return self._create_gate_common(pos, NotGate, **kwargs)

    def create_and_gate(self, pos, **kwargs) -> AndGate:
        return self._create_gate_common(pos, AndGate, **kwargs)

    def create_or_gate(self, pos, **kwargs) -> OrGate:
        return self._create_gate_common(pos, OrGate, **kwargs)

    def create_nand_gate(self, pos, **kwargs) -> NandGate:
        return self._create_gate_common(pos, NandGate, **kwargs)

    def create_nor_gate(self, pos, **kwargs) -> NorGate:
        return self._create_gate_common(pos, NorGate, **kwargs)

    def create_xor_gate(self, pos, **kwargs) -> XorGate:
        return self._create_gate_common(pos, XorGate, **kwargs)

    def connect_gates(self,
                      output_gate: LogicGate,
                      input_gate: LogicGate,
                      output_index: int = 0,
                      input_index: int = 0) -> Wire:
        """두 게이트를 와이어로 연결"""
        start_point = self.get_gate_output_coords(output_gate, output_index)
        end_point = self.get_gate_input_coords(input_gate, input_index)
        wire = self.create_wire(start_point, end_point)
        output_gate.connect_output_wire(wire, output_index)
        input_gate.connect_input_wire(wire, input_index)
        return wire

    def move_gate(self, gate, target_pos, run_time=1):
        """게이트를 새로운 위치로 이동하는 애니메이션들을 생성하여 반환"""
        target_screen_pos = self.c2p(*target_pos) if len(target_pos) == 3 else self.c2p(
            target_pos[0], target_pos[1], LogicGateStyle.DEFAULT_Z_COORD)

        # 게이트와 와이어를 함께 움직이는 애니메이션 그룹 생성
        wire_anims = []

        # 게이트가 이동하면서 매 프레임마다 와이어도 업데이트
        def update_wires(mob, alpha):
            # 현재 위치와 목표 위치 사이를 보간
            current_pos = mob.get_center() * (1 - alpha) + target_screen_pos * alpha
            mob.move_to(current_pos)
            # 연결된 와이어 업데이트
            mob.update_connected_wires()

        return UpdateFromAlphaFunc(gate, update_wires, run_time=run_time)

    def get_gate_input_coords(self,
                              gate: LogicGate,
                              index: int = 0) -> Tuple[float, float]:
        """게이트의 입력 연결점을 빵판 좌표계로 변환하여 (x, y) 튜플로 반환"""
        input_point = gate.get_input_point(index)
        coords = self.p2c(input_point)
        return (float(coords[0]), float(coords[1]))

    def get_gate_output_coords(self,
                               gate: LogicGate,
                               index: int = 0) -> Tuple[float, float]:
        """게이트의 출력 연결점을 빵판 좌표계로 변환하여 (x, y) 튜플로 반환"""
        output_point = gate.get_output_point(index)
        coords = self.p2c(output_point)
        return (float(coords[0]), float(coords[1]))

    def create_wire(self,
                    start_pos: tuple[float, float] | tuple[float, float, float],
                    end_pos: tuple[float, float] | tuple[float, float, float],
                    mid_points: Optional[List[np.ndarray]] = None,
                    color: ManimColor = LogicGateStyle.WIRE_COLOR) -> Wire:
        """빵판 좌표계 상의 두 점을 연결하는 와이어 생성"""
        # 좌표계 변환
        start_screen_pos = self.c2p(
            *start_pos) if len(start_pos) == 3 else self.c2p(start_pos[0], start_pos[1], 0)
        end_screen_pos = self.c2p(
            *end_pos) if len(end_pos) == 3 else self.c2p(end_pos[0], end_pos[1], 0)

        # 중간점들도 좌표계 변환
        transformed_mid_points = None
        if mid_points:
            transformed_mid_points = [
                self.c2p(*p) if len(p) == 3 else self.c2p(p[0], p[1], 0)
                for p in mid_points
            ]

        # Wire 객체 생성 및 스케일 적용
        wire = Wire(
            start_screen_pos, 
            end_screen_pos, 
            mid_points=transformed_mid_points,
            color=color
        )
        wire.scale_stroke_width(self.scale_factor)

        self.add(wire)
        return wire

    def create_label(self, text: str, pos: tuple[float, float], font_size: int = 24, offset: np.ndarray = None) -> Text:
        """빵판 좌표계 상의 위치에 텍스트 레이블 생성 (팩토리 메서드)

        Args:
            text: 레이블 텍스트
            pos: (x, y) 튜플 좌표
            font_size: 폰트 크기 (기본 24)
            offset: 추가 오프셋 (예: LEFT * 0.5)
        Returns:
            생성된 Text 객체
        """
        # 빵판의 스케일값을 반영
        adjusted_font_size = font_size * self.scale_factor
        if offset is None:
            offset = ORIGIN
        else:
            offset = offset * self.scale_factor

        label = Text(text, font_size=adjusted_font_size)
        base = self.c2p(*pos)
        label.move_to(base + offset)
        self.add(label)
        return label

    def shift_coords(self, coords, offset):
        """빵판 좌표를 지정된 오프셋만큼 이동한 새로운 좌표 반환"""
        if len(offset) == 2:
            return (coords[0] + offset[0], coords[1] + offset[1])
        return (coords[0] + offset[0], coords[1] + offset[1], coords[2] + offset[2])
