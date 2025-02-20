from manim import *
from common.logic_gate.logic_gate import LogicGate
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

    def _create_gate_body(self) -> VMobject:
        """AND 게이트의 기본 도형 생성 (D 모양)"""
        stroke_color = interpolate_color(
            self.color, WHITE, LogicGateStyle.DEFAULT_STROKE_LIGHTEN)

        # 기본 크기 설정
        h = self.size/2    # 높이의 절반
        w = self.size * LogicGateStyle.AND_GATE_WIDTH_RATIO  # 너비
        r = self.size * LogicGateStyle.AND_GATE_ARC_RATIO   # 반원 반지름

        # 해상도 기반 점 개수 계산
        arc_length = PI * r
        pixels_per_unit = config.frame_width * \
            config.pixel_width / (config.frame_x_radius * 2)
        points_per_pixel = 0.5  # 픽셀당 점의 개수 (부드러운 곡선을 위해)
        num_points = int(arc_length * pixels_per_unit * points_per_pixel)
        num_points = max(20, min(num_points, 100))  # 제한

        points = []
        # 왼쪽 상단에서 시작하여 반시계 방향으로 점들을 추가
        points.append([-w, h, 0])      # 왼쪽 상단
        points.append([-w, -h, 0])     # 왼쪽 하단

        # 반원 부분 (아래에서 위로)
        for i in range(num_points + 1):
            theta = -PI/2 + (i/num_points) * PI
            x = r * np.cos(theta) + w
            y = r * np.sin(theta)
            points.append([x, y, 0])

        # 경로 닫기
        points.append([-w, h, 0])

        return Polygon(
            *points,
            color=stroke_color,
            stroke_width=LogicGateStyle.DEFAULT_STROKE_WIDTH,
            fill_color=self.color,
            fill_opacity=LogicGateStyle.DEFAULT_FILL_OPACITY
        )
