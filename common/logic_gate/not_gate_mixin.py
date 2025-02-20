from manim import *
from common.logic_gate.styles import LogicGateStyle


class NotGateMixin:
    """NOT 게이트의 출력 원을 추가하는 믹스인 클래스"""

    def _add_not_circle(self) -> None:
        """NOT을 표현하는 출력 원 추가 및 출력 포트 조정"""
        circle = self._create_output_circle()
        self.add(circle)
        self.output_ports[0].move_to(circle.get_right())

    def _create_output_circle(self, circle_ratio: float, body_right_x: float) -> Circle:
        """출력 부분의 NOT 원형 생성"""
        stroke_color = interpolate_color(
            self.color, WHITE, LogicGateStyle.DEFAULT_STROKE_LIGHTEN)
        circle_radius = self.size * circle_ratio

        # 원의 중심을 게이트 본체의 오른쪽 끝에서 circle_radius만큼 이동
        circle_x = body_right_x + circle_radius

        return Circle(
            radius=circle_radius,
            color=stroke_color,
            stroke_width=LogicGateStyle.DEFAULT_STROKE_WIDTH,
            fill_color=self.color,
            fill_opacity=LogicGateStyle.DEFAULT_FILL_OPACITY
        ).move_to(RIGHT * circle_x)
