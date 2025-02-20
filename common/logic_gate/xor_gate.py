from manim import *
from common.logic_gate.or_gate import OrGate
from common.logic_gate.styles import LogicGateStyle


class XorGate(OrGate):
    """XOR 게이트 (OR 게이트 + 추가 입력단 곡선)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_extra_curve()

    def _setup_extra_curve(self) -> None:
        """추가 곡선 설정 및 입력 포트 재배치"""
        extra_curve = self._create_extra_curve()
        self.add_to_back(extra_curve)
        self._adjust_input_ports()

    def _create_extra_curve(self) -> VMobject:
        """XOR 게이트의 추가 입력단 곡선 생성"""
        return VMobject(
            stroke_color=self._get_stroke_color(),
            stroke_width=LogicGateStyle.XOR_GATE_EXTRA_CURVE_WIDTH,
            fill_opacity=0
        ).set_points_as_corners(self._calculate_extra_curve_points())

    def _get_stroke_color(self) -> ManimColor:
        """곡선의 stroke 색상 계산"""
        return interpolate_color(
            self.color,
            WHITE,
            LogicGateStyle.DEFAULT_STROKE_LIGHTEN
        )

    def _calculate_extra_curve_points(self) -> list:
        """추가 곡선을 이루는 점들의 위치 계산"""
        h = self.size/2
        w = self.size * LogicGateStyle.XOR_GATE_WIDTH_RATIO
        curve_depth = self.size * LogicGateStyle.XOR_GATE_CURVE_DEPTH
        offset = self.size * LogicGateStyle.XOR_GATE_EXTRA_CURVE_OFFSET

        points = []
        num_points = self._calculate_resolution(h)

        for i in range(num_points // 2):
            t = i / (num_points // 2)
            y = h * (1 - 2 * t)
            x = (-w - offset) + curve_depth * (4 * t * (1 - t))
            points.append([x, y, 0])

        return points

    def _calculate_resolution(self, height: float) -> int:
        """곡선의 해상도(점 개수) 계산"""
        arc_length = PI * height * 2
        pixels_per_unit = config.frame_width * \
            config.pixel_width / (config.frame_x_radius * 2)
        num_points = int(arc_length * pixels_per_unit * 0.5)
        return max(30, min(num_points, 120))

    def _adjust_input_ports(self) -> None:
        """입력 포트들의 위치를 extra curve에 맞게 재조정"""
        h = self.size/2
        w = self.size * LogicGateStyle.XOR_GATE_WIDTH_RATIO
        offset = self.size * LogicGateStyle.XOR_GATE_EXTRA_CURVE_OFFSET
        port_y_ratio = LogicGateStyle.PORT_VERTICAL_SPACING * \
            LogicGateStyle.XOR_GATE_PORT_SPACING
        curve_depth = self.size * LogicGateStyle.XOR_GATE_CURVE_DEPTH

        # 상/하단 포트의 t 값 계산
        t_up = (1 - port_y_ratio) / 2
        t_down = (1 + port_y_ratio) / 2

        # 각 포트의 새로운 위치 계산 및 이동
        for i, t in enumerate([t_up, t_down]):
            x = -w - offset + curve_depth * (4 * t * (1 - t))
            y = h * port_y_ratio * (1 if i == 0 else -1)
            self.input_ports[i].move_to([x, y, 0])
