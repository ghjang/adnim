from manim import *
from common.logic_gate.styles import LogicGateStyle


class LogicGate(VGroup):
    """논리 게이트들의 기본 클래스"""

    def __init__(self,
                 color=LogicGateStyle.DEFAULT_COLOR,
                 size=LogicGateStyle.DEFAULT_SIZE,
                 **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.color = color
        self.input_ports = []
        self.output_ports = []
        self.input_wires = []    # 입력 와이어 목록
        self.output_wires = []   # 출력 와이어 목록

    def _create_port(self, position):
        """입출력 포트 생성"""
        port = Dot(
            radius=self.size * LogicGateStyle.PORT_RADIUS,
            color=self.color,
        ).set_style(**LogicGateStyle.PORT_STYLE).move_to(position)
        return port

    def get_input_points(self):
        """모든 입력 연결점 리스트 반환"""
        return [port.get_center() for port in self.input_ports]

    def get_output_points(self):
        """모든 출력 연결점 리스트 반환"""
        return [port.get_center() for port in self.output_ports]

    def get_input_point(self, index=0):
        """특정 인덱스의 입력 연결점 반환"""
        return self.input_ports[index].get_center()

    def get_output_point(self, index=0):
        """특정 인덱스의 출력 연결점 반환"""
        return self.output_ports[index].get_center()

    def connect_input_wire(self, wire, index=0):
        """입력 와이어 연결"""
        if index >= len(self.input_ports):
            raise IndexError("Invalid input port index")
        self.input_wires.append(wire)
        wire.set_end_gate(self, index)
        return self
    
    def connect_output_wire(self, wire, index=0):
        """출력 와이어 연결"""
        if index >= len(self.output_ports):
            raise IndexError("Invalid output port index")
        self.output_wires.append(wire)
        wire.set_start_gate(self, index)
        return self

    def update_connected_wires(self):
        """연결된 모든 와이어의 위치 업데이트"""
        for wire in self.input_wires:
            wire.update_end_position()
        for wire in self.output_wires:
            wire.update_start_position()
