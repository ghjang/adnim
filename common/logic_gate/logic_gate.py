from __future__ import annotations
from typing import List
from manim import *
from common.logic_gate.styles import LogicGateStyle
from common.logic_gate.base_interfaces import LogicGateBase, WireBase


class LogicGate(VGroup, LogicGateBase):
    """논리 게이트들의 기본 클래스"""

    def __init__(self,
                 color: ManimColor = LogicGateStyle.DEFAULT_COLOR,
                 size: float = LogicGateStyle.DEFAULT_SIZE,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.size: float = size
        self.color: ManimColor = color
        self.input_ports: List[Dot] = []
        self.output_ports: List[Dot] = []
        self.input_wires: List[WireBase] = []    # 입력 와이어 목록
        self.output_wires: List[WireBase] = []   # 출력 와이어 목록

    def _create_port(self, position: np.ndarray) -> Dot:
        """입출력 포트 생성"""
        port = Dot(
            radius=self.size * LogicGateStyle.PORT_RADIUS,
            color=self.color,
        ).set_style(**LogicGateStyle.PORT_STYLE).move_to(position)
        return port

    def get_input_points(self) -> List[np.ndarray]:
        """모든 입력 연결점 리스트 반환"""
        return [port.get_center() for port in self.input_ports]

    def get_output_points(self) -> List[np.ndarray]:
        """모든 출력 연결점 리스트 반환"""
        return [port.get_center() for port in self.output_ports]

    def get_input_point(self, index: int = 0) -> np.ndarray:
        """특정 인덱스의 입력 연결점 반환"""
        return self.input_ports[index].get_center()

    def get_output_point(self, index: int = 0) -> np.ndarray:
        """특정 인덱스의 출력 연결점 반환"""
        return self.output_ports[index].get_center()

    def connect_input_wire(self, wire: WireBase, index: int = 0) -> LogicGate:
        """입력 와이어 연결"""
        if index >= len(self.input_ports):
            raise IndexError("Invalid input port index")
        self.input_wires.append(wire)
        wire.set_end_gate(self, index)
        return self

    def connect_output_wire(self, wire: WireBase, index: int = 0) -> LogicGate:
        """출력 와이어 연결"""
        if index >= len(self.output_ports):
            raise IndexError("Invalid output port index")
        self.output_wires.append(wire)
        wire.set_start_gate(self, index)
        return self

    def update_connected_wires(self) -> None:
        """연결된 모든 와이어의 위치 업데이트"""
        for wire in self.input_wires:
            wire.update_end_position()
        for wire in self.output_wires:
            wire.update_start_position()
