from manim import *
from typing import List, Dict
from common.logic_gate.logic_gate import LogicGate
from common.logic_gate.wire import Wire


class CompositeGate(LogicGate):
    """복합 게이트 기본 클래스"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.internal_gates: List[LogicGate] = []
        self.internal_wires: List[Wire] = []
        self.port_mappings: Dict[str, Dot] = {}  # 외부 포트 매핑

    def add_internal_gate(self, gate: LogicGate) -> None:
        """내부 게이트 추가"""
        self.internal_gates.append(gate)
        self.add(gate)

    def add_internal_wire(self, wire: Wire) -> None:
        """내부 와이어 추가"""
        self.internal_wires.append(wire)
        self.add(wire)

    def map_external_port(self, port_name: str, port: Dot) -> None:
        """외부 포트 매핑 추가"""
        self.port_mappings[port_name] = port
        if port_name.startswith('input'):
            self.input_ports.append(port)
        elif port_name.startswith('output'):
            self.output_ports.append(port)
        self.add(port)

    def get_port_by_name(self, port_name: str) -> Dot:
        """이름으로 포트 가져오기"""
        return self.port_mappings.get(port_name)

    def update_connected_wires(self) -> None:
        """모든 내부 게이트의 와이어 업데이트"""
        super().update_connected_wires()
        for gate in self.internal_gates:
            gate.update_connected_wires()
