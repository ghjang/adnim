from manim import *
from common.logic_gate.not_gate import NotGate
from common.logic_gate.bread_board import BreadBoardPlane


class NotGateTestScene(Scene):
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
