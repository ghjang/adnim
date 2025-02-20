import numpy as np
from manim import *
from common.logic_gate.styles import LogicGateStyle
from common.logic_gate.logic_gate import LogicGate


class NotGate(LogicGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 기본 도형 생성
        triangle = self._create_triangle()
        circle = self._create_circle()

        # 입출력 포트 생성 및 저장
        self.input_ports.append(self._create_port(triangle.get_left()))
        self.output_ports.append(self._create_port(circle.get_right()))

        self.add(triangle, circle, *self.input_ports, *self.output_ports)

    def _create_triangle(self) -> Polygon:
        stroke_color = interpolate_color(
            self.color, WHITE, LogicGateStyle.DEFAULT_STROKE_LIGHTEN)
        return Polygon(
            np.array([-self.size/2, self.size/2,
                     LogicGateStyle.DEFAULT_Z_COORD]),
            np.array([-self.size/2, -self.size/2,
                     LogicGateStyle.DEFAULT_Z_COORD]),
            np.array([self.size/2, 0, LogicGateStyle.DEFAULT_Z_COORD])
        ).set_stroke(color=stroke_color, width=LogicGateStyle.DEFAULT_STROKE_WIDTH
                     ).set_fill(self.color, opacity=LogicGateStyle.DEFAULT_FILL_OPACITY)

    def _create_circle(self) -> Circle:
        stroke_color = interpolate_color(
            self.color, WHITE, LogicGateStyle.DEFAULT_STROKE_LIGHTEN)
        circle_radius = self.size * LogicGateStyle.DEFAULT_CIRCLE_RATIO
        offset = self.size * (0.5 + LogicGateStyle.CIRCLE_OFFSET_RATIO)

        return Circle(radius=circle_radius).move_to(
            RIGHT * offset
        ).set_stroke(color=stroke_color, width=LogicGateStyle.DEFAULT_STROKE_WIDTH
                     ).set_fill(self.color, opacity=LogicGateStyle.DEFAULT_FILL_OPACITY)
