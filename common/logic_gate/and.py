from manim import *
from common.logic_gate.base import LogicGate
from common.logic_gate.styles import LogicGateStyle


class AndGate(LogicGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 기본 도형 생성
        body = self._create_gate_body()

        # 두 개의 입력 포트와 하나의 출력 포트 생성
        input_port1 = self._create_port(
            body.get_left() + UP * self.size * LogicGateStyle.PORT_VERTICAL_SPACING)
        input_port2 = self._create_port(
            body.get_left() + DOWN * self.size * LogicGateStyle.PORT_VERTICAL_SPACING)
        output_port = self._create_port(body.get_right())

        # 포트들을 리스트에 순서대로 추가
        self.input_ports.extend([input_port1, input_port2])
        self.output_ports.append(output_port)

        self.add(body, *self.input_ports, *self.output_ports)
