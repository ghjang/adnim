from manim import *
from common.logic_gate.and_gate import AndGate
from common.logic_gate.styles import LogicGateStyle
from common.logic_gate.not_gate_mixin import NotGateMixin


class NandGate(AndGate, NotGateMixin):
    """NAND 게이트 (AND 게이트 + NOT의 원형)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        body_right_x = self.size * (
            LogicGateStyle.AND_GATE_WIDTH_RATIO +
            LogicGateStyle.AND_GATE_ARC_RATIO
        )
        circle = self._create_output_circle(
            LogicGateStyle.NAND_GATE_CIRCLE_RATIO,
            body_right_x
        )
        self.add(circle)
        self.output_ports[0].move_to(circle.get_right())
