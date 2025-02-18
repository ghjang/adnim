from manim import *
import numpy as np
from common.logic_gate.styles import LogicGateStyle
from common.logic_gate.base import LogicGate
from common.logic_gate.wire import Wire


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

    def _create_triangle(self):
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

    def _create_circle(self):
        stroke_color = interpolate_color(
            self.color, WHITE, LogicGateStyle.DEFAULT_STROKE_LIGHTEN)
        circle_radius = self.size * LogicGateStyle.DEFAULT_CIRCLE_RATIO
        offset = self.size * (0.5 + LogicGateStyle.CIRCLE_OFFSET_RATIO)

        return Circle(radius=circle_radius).move_to(
            RIGHT * offset
        ).set_stroke(color=stroke_color, width=LogicGateStyle.DEFAULT_STROKE_WIDTH
                     ).set_fill(self.color, opacity=LogicGateStyle.DEFAULT_FILL_OPACITY)


class BreadBoardPlane(NumberPlane):
    # 스타일 상수 정의
    AXIS_STYLE = {
        "color": GREY_C,
        "stroke_opacity": 0.3
    }
    GRID_STYLE = {
        "stroke_color": GREY_B,
        "stroke_width": 1,
        "stroke_opacity": 0.3
    }

    def __init__(self, **kwargs):
        super().__init__(
            axis_config=self.AXIS_STYLE,
            x_axis_config=self.AXIS_STYLE,
            y_axis_config=self.AXIS_STYLE,
            background_line_style=self.GRID_STYLE,
            **kwargs
        )
        self.scale_factor = 1
        self.shift_vector = ORIGIN

    # shift를 오버라이드하여 shift_vector 기록
    def shift(self, vector, **kwargs):
        result = super().shift(vector, **kwargs)
        self.shift_vector = getattr(self, "shift_vector", ORIGIN) + vector
        return result

    # 스케일 적용 시 scale_factor 저장
    def scale(self, factor, **kwargs):
        self.scale_factor = factor
        return super().scale(factor, **kwargs)

    def create_not_gate(self, pos, **kwargs):
        scaled_size = kwargs.get(
            'size', LogicGateStyle.DEFAULT_SIZE) * self.scale_factor
        kwargs['size'] = scaled_size

        screen_pos = self.c2p(*pos) if len(pos) == 3 else self.c2p(
            pos[0], pos[1], LogicGateStyle.DEFAULT_Z_COORD)

        not_gate = NotGate(**kwargs).move_to(screen_pos)
        self.add(not_gate)
        return not_gate

    def connect_gates(self, output_gate, input_gate, output_index=0, input_index=0):
        """두 게이트를 와이어로 연결"""
        start_point = self.get_gate_output_coords(output_gate, output_index)
        end_point = self.get_gate_input_coords(input_gate, input_index)
        wire = self.create_wire(start_point, end_point)
        output_gate.connect_output_wire(wire, output_index)
        input_gate.connect_input_wire(wire, input_index)
        return wire

    def move_gate(self, gate, target_pos, run_time=1):
        """게이트를 새로운 위치로 이동하는 애니메이션들을 생성하여 반환"""
        target_screen_pos = self.c2p(*target_pos) if len(target_pos) == 3 else self.c2p(
            target_pos[0], target_pos[1], LogicGateStyle.DEFAULT_Z_COORD)

        # 게이트와 와이어를 함께 움직이는 애니메이션 그룹 생성
        wire_anims = []

        # 게이트가 이동하면서 매 프레임마다 와이어도 업데이트
        def update_wires(mob, alpha):
            # 현재 위치와 목표 위치 사이를 보간
            current_pos = mob.get_center() * (1 - alpha) + target_screen_pos * alpha
            mob.move_to(current_pos)
            # 연결된 와이어 업데이트
            mob.update_connected_wires()

        return UpdateFromAlphaFunc(gate, update_wires, run_time=run_time)

    def get_gate_input_coords(self, gate, index=0):
        """게이트의 입력 연결점을 빵판 좌표계로 변환하여 (x, y) 튜플로 반환"""
        input_point = gate.get_input_point(index)
        coords = self.p2c(input_point)
        return (float(coords[0]), float(coords[1]))

    def get_gate_output_coords(self, gate, index=0):
        """게이트의 출력 연결점을 빵판 좌표계로 변환하여 (x, y) 튜플로 반환"""
        output_point = gate.get_output_point(index)
        coords = self.p2c(output_point)
        return (float(coords[0]), float(coords[1]))

    def create_wire(self, start_pos, end_pos, color=LogicGateStyle.WIRE_COLOR):
        """빵판 좌표계 상의 두 점을 연결하는 와이어 생성"""
        # 좌표계 변환
        start_screen_pos = self.c2p(
            *start_pos) if len(start_pos) == 3 else self.c2p(start_pos[0], start_pos[1], 0)
        end_screen_pos = self.c2p(
            *end_pos) if len(end_pos) == 3 else self.c2p(end_pos[0], end_pos[1], 0)

        # Wire 객체 생성 및 스케일 적용
        wire = Wire(start_screen_pos, end_screen_pos, color=color)
        wire.scale_stroke_width(self.scale_factor)

        self.add(wire)
        return wire

    def shift_coords(self, coords, offset):
        """빵판 좌표를 지정된 오프셋만큼 이동한 새로운 좌표 반환"""
        if len(offset) == 2:
            return (coords[0] + offset[0], coords[1] + offset[1])
        return (coords[0] + offset[0], coords[1] + offset[1], coords[2] + offset[2])

    def get_wire_start_coords(self, wire):
        """와이어의 시작점을 빵판 좌표계로 변환하여 (x, y) 튜플로 반환"""
        start_point = wire.get_start_point()
        coords = self.p2c(start_point)
        return (float(coords[0]), float(coords[1]))

    def get_wire_end_coords(self, wire):
        """와이어의 끝점을 빵판 좌표계로 변환하여 (x, y) 튜플로 반환"""
        end_point = wire.get_end_point()
        coords = self.p2c(end_point)
        return (float(coords[0]), float(coords[1]))


class NotGateScene(Scene):
    def construct(self):
        # 좌측에 NotGate 배치
        left_gate = NotGate().to_edge(LEFT).shift(RIGHT * 2).scale(2)
        self.play(FadeIn(left_gate))

        # 우측에 NumberPlane 생성 및 위치 이동
        plane = BreadBoardPlane().shift(RIGHT*3).scale(0.5)

        # plane 내부 좌표 (1,1)에 NotGate 배치 후 (2,2)로 이동 애니메이션
        right_gate = plane.create_not_gate((1, 1))

        input_point = plane.get_gate_input_coords(right_gate)
        # 입력 포인트에서 왼쪽으로 1만큼 이동한 좌표 생성
        start_point = plane.shift_coords(input_point, (-5, 0))
        input_wire = plane.create_wire(start_point, input_point)
        right_gate.connect_input_wire(input_wire)

        output_point = plane.get_gate_output_coords(right_gate)
        end_point = plane.shift_coords(output_point, (5, 0))
        output_wire = plane.create_wire(output_point, end_point)
        right_gate.connect_output_wire(output_wire)

        self.play(FadeOut(left_gate), FadeIn(plane))

        # 스케일 애니메이션
        self.play(
            plane.animate.move_to(ORIGIN).scale(2)
        )
        self.wait(1)

        # 이동 애니메이션 실행 (수정된 부분)
        gate_movement = plane.move_gate(right_gate, (3, 0))
        self.play(gate_movement)
        self.wait(1)

        # 게이트의 입출력 연결점 좌표 확인 (이제 x, y 좌표가 튜플로 반환됨)
        input_coords = plane.get_gate_input_coords(right_gate)
        output_coords = plane.get_gate_output_coords(right_gate)
        print(f"Input coords (x,y): {input_coords}")
        print(f"Output coords (x,y): {output_coords}")
