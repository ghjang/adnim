from manim import *
from common.logic_gate.bread_board import BreadBoardPlane
from common.logic_gate.wire import Wire
from common.logic_gate.composite_gate import CompositeGate
from common.logic_gate.composite_gate_builder import CompositeGateBuilder


class HalfAdderTestScene(Scene):
    """반가산기 테스트 씬"""

    def construct(self):
        # 빵판 생성 및 반가산기 배치
        plane = BreadBoardPlane()
        self.add(plane)

        # 반가산기 생성
        builder = CompositeGateBuilder(plane)
        half_adder = builder.build_half_adder((0, 0), color=BLUE)

        # 바운딩 박스 생성 (점선 스타일)
        box = builder.build_bounding_box(half_adder)

        self.wait(2)

        # 와이어 생성 및 좌표 저장
        input_wires, input_points = self._create_input_wires(plane, half_adder)
        output_wires, output_points = self._create_output_wires(
            plane, half_adder
        )

        # 저장된 좌표로 라벨 생성
        labels = VGroup(
            plane.create_label("A", input_points[0], offset=LEFT * 0.5),
            plane.create_label("B", input_points[1], offset=LEFT * 0.5),
            plane.create_label("S", output_points[0], offset=RIGHT * 0.5),
            plane.create_label("C", output_points[1], offset=RIGHT * 0.5)
        )

        # 애니메이션
        # self.play(Create(VGroup(*input_wires, *output_wires)))
        # self.play(Write(labels))
        self.wait(3)

    def _create_external_wires(self, plane: BreadBoardPlane, adder: CompositeGate) -> list[Wire]:
        """외부 연결 와이어 생성"""
        # 입력 와이어 생성
        input_wires = self._create_input_wires(plane, adder)
        # 출력 와이어 생성
        output_wires = self._create_output_wires(plane, adder)

        return [*input_wires, *output_wires]

    def _create_input_wires(self, plane: BreadBoardPlane, adder: CompositeGate) -> tuple[list[Wire], list[tuple]]:
        """입력 와이어 생성 및 시작점 좌표 반환"""
        input_coords = {
            'a': {'port': 'input_a', 'offset': -1},
            'b': {'port': 'input_b', 'offset': -1}
        }

        wires = []
        start_points = []
        for port_name, info in input_coords.items():
            end_point = adder.get_port_by_name(info['port']).get_center()
            start_point = (
                end_point[0] + info['offset'],
                end_point[1],
            )
            wire = plane.create_wire(end_point, start_point)
            wires.append(wire)
            start_points.append(start_point)

        return wires, start_points

    def _create_output_wires(self, plane: BreadBoardPlane, adder: CompositeGate) -> tuple[list[Wire], list[tuple]]:
        """출력 와이어 생성 및 끝점 좌표 반환"""
        output_coords = {
            'sum': {'port': 'output_sum', 'offset': 1},
            'carry': {'port': 'output_carry', 'offset': 1}
        }

        wires = []
        end_points = []
        for port_name, info in output_coords.items():
            start_point = adder.get_port_by_name(info['port']).get_center()
            end_point = (
                start_point[0] + info['offset'],
                start_point[1],
            )
            wire = plane.create_wire(start_point, end_point)
            wires.append(wire)
            end_points.append(end_point)

        return wires, end_points

    def _create_port_labels(self, plane: BreadBoardPlane, wires: list[Wire]) -> VGroup:
        """입출력 포트 라벨 생성"""
        # 입력 A, B / 출력 S, C 순서로 와이어가 저장되어 있음
        input_a_pos = (wires[0].get_start()[0], wires[0].get_start()[1])
        input_b_pos = (wires[1].get_start()[0], wires[1].get_start()[1])
        sum_pos = (wires[2].get_end()[0], wires[2].get_end()[1])
        carry_pos = (wires[3].get_end()[0], wires[3].get_end()[1])

        return VGroup(
            plane.create_label("A", input_a_pos, offset=LEFT * 0.5),
            plane.create_label("B", input_b_pos, offset=LEFT * 0.5),
            plane.create_label("S", sum_pos, offset=RIGHT * 0.5),
            plane.create_label("C", carry_pos, offset=RIGHT * 0.5)
        )
