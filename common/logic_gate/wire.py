from __future__ import annotations
from typing import Optional
from manim import *
from common.logic_gate.styles import LogicGateStyle
from common.logic_gate.base_interfaces import LogicGateBase, WireBase


class Wire(VGroup, WireBase):
    """논리 회로의 연결선을 표현하는 클래스"""

    def __init__(self,
                 start_pos: np.ndarray,
                 end_pos: np.ndarray,
                 color: ManimColor = LogicGateStyle.WIRE_COLOR,
                 stroke_width: float = LogicGateStyle.WIRE_STROKE_WIDTH,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.start_pos: np.ndarray = start_pos
        self.end_pos: np.ndarray = end_pos
        self.wire_color: ManimColor = color
        self.wire_stroke_width: float = stroke_width
        self.wire_line: Line = self._create_wire()
        self.start_gate: Optional[LogicGateBase] = None
        self.end_gate: Optional[LogicGateBase] = None
        self.start_port_index: int = 0
        self.end_port_index: int = 0
        self.add(self.wire_line)

    def _create_wire(self) -> Line:
        """기본 직선 와이어 생성"""
        return Line(
            self.start_pos,
            self.end_pos,
            color=self.wire_color,
            stroke_width=self.wire_stroke_width,
            stroke_opacity=LogicGateStyle.WIRE_OPACITY
        )

    def scale_stroke_width(self, scale_factor: float) -> Wire:
        """스케일에 맞춰 선 두께 조정"""
        self.wire_stroke_width = self.wire_stroke_width / scale_factor
        self.wire_line.set_stroke(width=self.wire_stroke_width)
        return self

    def get_start_point(self) -> np.ndarray:
        """와이어의 시작점 위치 반환"""
        return self.wire_line.get_start()

    def get_end_point(self) -> np.ndarray:
        """와이어의 끝점 위치 반환"""
        return self.wire_line.get_end()

    def set_start_gate(self, gate: LogicGateBase, port_index: int = 0) -> None:
        """와이어 시작점에 게이트 연결"""
        self.start_gate = gate
        self.start_port_index = port_index
        self.update_start_position()

    def set_end_gate(self, gate: LogicGateBase, port_index: int = 0) -> None:
        """와이어 끝점에 게이트 연결"""
        self.end_gate = gate
        self.end_port_index = port_index
        self.update_end_position()

    def update_start_position(self) -> None:
        """시작점 위치 업데이트"""
        if self.start_gate:
            new_start = self.start_gate.get_output_point(self.start_port_index)
            self.wire_line.put_start_and_end_on(
                new_start, self.wire_line.get_end())

    def update_end_position(self) -> None:
        """끝점 위치 업데이트"""
        if self.end_gate:
            new_end = self.end_gate.get_input_point(self.end_port_index)
            self.wire_line.put_start_and_end_on(
                self.wire_line.get_start(), new_end)
