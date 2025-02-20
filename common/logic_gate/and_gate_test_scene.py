from manim import *
from common.logic_gate.and_gate import AndGate
from common.logic_gate.bread_board import BreadBoardPlane


class AndGateTestScene(Scene):
    def construct(self):
        # 좌측에 AndGate 배치
        left_gate = AndGate().to_edge(LEFT).shift(RIGHT * 2).scale(2)
        self.play(FadeIn(left_gate))

        # 우측에 NumberPlane 생성 및 위치 이동
        plane = BreadBoardPlane().shift(RIGHT*3).scale(0.5)

        # plane 내부에 AndGate 배치
        right_gate = plane.create_and_gate((1, 1))

        # 첫 번째 입력 와이어 생성 및 연결
        input_point1 = plane.get_gate_input_coords(
            right_gate, index=0)  # 상단 입력
        start_point1 = plane.shift_coords(input_point1, (-5, 2))
        input_wire1 = plane.create_wire(start_point1, input_point1)
        right_gate.connect_input_wire(input_wire1, index=0)

        # 두 번째 입력 와이어 생성 및 연결
        input_point2 = plane.get_gate_input_coords(
            right_gate, index=1)  # 하단 입력
        start_point2 = plane.shift_coords(input_point2, (-5, -2))
        input_wire2 = plane.create_wire(start_point2, input_point2)
        right_gate.connect_input_wire(input_wire2, index=1)

        # 출력 와이어 생성 및 연결
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

        # 이동 애니메이션
        gate_movement = plane.move_gate(right_gate, (3, 0))
        self.play(gate_movement)
        self.wait(1)

        # 게이트의 입출력 연결점 좌표 출력
        for i in range(2):
            input_coords = plane.get_gate_input_coords(right_gate, i)
            print(f"Input {i+1} coords (x,y): {input_coords}")
        output_coords = plane.get_gate_output_coords(right_gate)
        print(f"Output coords (x,y): {output_coords}")
