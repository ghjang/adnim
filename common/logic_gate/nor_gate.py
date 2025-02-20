from manim import *
from common.logic_gate.or_gate import OrGate
from common.logic_gate.styles import LogicGateStyle
from common.logic_gate.not_gate_mixin import NotGateMixin


class NorGate(OrGate, NotGateMixin):
    """NOR 게이트 (OR 게이트 + NOT의 원형)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        body_right_x = self.size * (
            LogicGateStyle.OR_GATE_WIDTH_RATIO + 0.5
        )
        circle = self._create_output_circle(
            LogicGateStyle.NOR_GATE_CIRCLE_RATIO,
            body_right_x
        )
        self.add(circle)
        self.output_ports[0].move_to(circle.get_right())
