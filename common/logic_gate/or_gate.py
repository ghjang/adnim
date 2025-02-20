from manim import *
from common.logic_gate.logic_gate import LogicGate
from common.logic_gate.styles import LogicGateStyle

class OrGate(LogicGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        body = self._create_gate_body()
        
        # 입력 포트 위치 계산 및 생성
        input_ports = self._create_input_ports(body)
        output_port = self._create_port(body.get_right())

        # 포트들을 리스트에 추가
        self.input_ports.extend(input_ports)
        self.output_ports.append(output_port)
        
        # 모든 요소를 그룹에 추가
        self.add(body, *self.input_ports, *self.output_ports)

    def _create_input_ports(self, body: VMobject) -> list[Dot]:
        """입력 포트들의 위치를 계산하고 생성"""
        h = self.size/2
        w = self.size * LogicGateStyle.OR_GATE_WIDTH_RATIO
        port_y_ratio = LogicGateStyle.PORT_VERTICAL_SPACING * LogicGateStyle.OR_GATE_PORT_SPACING
        curve_depth = self.size * LogicGateStyle.OR_GATE_CURVE_DEPTH

        # 상/하단 포트의 t 값 계산
        t_up = (1 - port_y_ratio) / 2
        t_down = (1 + port_y_ratio) / 2

        # 곡선 상의 x 좌표 계산
        port1_x = -w + curve_depth * (4 * t_up * (1 - t_up))
        port2_x = -w + curve_depth * (4 * t_down * (1 - t_down))

        # 포트 생성
        return [
            self._create_port(np.array([port1_x, h * port_y_ratio, 0])),
            self._create_port(np.array([port2_x, -h * port_y_ratio, 0]))
        ]

    def _create_gate_body(self) -> VMobject:
        """OR 게이트의 기본 도형 생성 (둥근 D 모양)"""
        # 기본 크기 설정
        h = self.size/2
        w = self.size * LogicGateStyle.OR_GATE_WIDTH_RATIO
        curve_depth = self.size * LogicGateStyle.OR_GATE_CURVE_DEPTH

        # 해상도 기반 점 개수 계산
        num_points = self._calculate_curve_points(h)
        points = []

        # 왼쪽 곡선부 생성 (위에서 아래로)
        points.extend(self._create_left_curve_points(h, w, curve_depth, num_points))
        
        # 오른쪽 반원부 생성 (아래에서 위로)
        points.extend(self._create_right_arc_points(h, w, num_points))

        return self._create_polygon_from_points(points)

    def _calculate_curve_points(self, height: float) -> int:
        """곡선을 그리기 위한 점의 개수 계산"""
        arc_length = PI * height * 2
        pixels_per_unit = config.frame_width * config.pixel_width / (config.frame_x_radius * 2)
        num_points = int(arc_length * pixels_per_unit * 0.5)
        return max(30, min(num_points, 120))

    def _create_left_curve_points(self, h: float, w: float, curve_depth: float, num_points: int) -> list:
        """왼쪽 곡선부의 점들 생성"""
        points = []
        for i in range(num_points // 2):
            t = i / (num_points // 2)
            y = h * (1 - 2 * t)
            x = -w + curve_depth * (4 * t * (1 - t))
            points.append([x, y, 0])
        return points

    def _create_right_arc_points(self, h: float, w: float, num_points: int) -> list:
        """오른쪽 반원부의 점들 생성"""
        points = []
        for i in range(num_points // 2 + 1):
            theta = -PI/2 + (i/(num_points/2)) * PI
            x = w + h * np.cos(theta)
            y = h * np.sin(theta)
            points.append([x, y, 0])
        return points

    def _create_polygon_from_points(self, points: list) -> Polygon:
        """주어진 점들로 폴리곤 생성"""
        stroke_color = interpolate_color(
            self.color, WHITE, LogicGateStyle.DEFAULT_STROKE_LIGHTEN)
        
        return Polygon(
            *points,
            color=stroke_color,
            stroke_width=LogicGateStyle.DEFAULT_STROKE_WIDTH,
            fill_color=self.color,
            fill_opacity=LogicGateStyle.DEFAULT_FILL_OPACITY
        )
