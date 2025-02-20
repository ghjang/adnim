from manim import *
from common.logic_gate.or_gate import OrGate
from common.logic_gate.styles import LogicGateStyle


class NorGate(OrGate):
    """NOR 게이트 (OR 게이트 + NOT의 원형)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._add_not_circle()

    def _add_not_circle(self) -> None:
        """NOT을 표현하는 출력 원 추가 및 출력 포트 조정"""
        circle = self._create_output_circle()
        self.add(circle)
        self.output_ports[0].move_to(circle.get_right())

    def _create_output_circle(self) -> Circle:
        """출력 부분의 NOT 원형 생성"""
        stroke_color = interpolate_color(
            self.color, WHITE, LogicGateStyle.DEFAULT_STROKE_LIGHTEN)
        circle_radius = self.size * LogicGateStyle.NOR_GATE_CIRCLE_RATIO

        # OR 게이트 본체의 오른쪽 반원 중심 x좌표 계산
        body_right_x = self.size * (
            LogicGateStyle.OR_GATE_WIDTH_RATIO + 0.5  # 0.5는 반원의 반지름 비율
        )

        # 원의 중심을 OR 게이트 본체의 오른쪽 끝에서 정확히 circle_radius만큼 이동
        circle_x = body_right_x + circle_radius

        return Circle(
            radius=circle_radius,
            color=stroke_color,
            stroke_width=LogicGateStyle.DEFAULT_STROKE_WIDTH,
            fill_color=self.color,
            fill_opacity=LogicGateStyle.DEFAULT_FILL_OPACITY
        ).move_to(RIGHT * circle_x)
