from manim import *
from common.logic_gate.bread_board import BreadBoardPlane
from common.logic_gate.wire import Wire
from common.logic_gate.composite_gate import CompositeGate
from common.logic_gate.composite_gate_builder import CompositeGateBuilder


class NandXorTestScene(Scene):
    """NAND로 구성된 XOR 게이트 테스트 씬"""

    def construct(self):
        # 빵판 생성 및 XOR 게이트 배치
        plane = BreadBoardPlane()
        self.add(plane)

        # NAND-XOR 게이트 생성
        builder = CompositeGateBuilder(plane)
        xor_gate = builder.build_nand_xor((0, 0), color=BLUE)

        # 바운딩 박스 생성
        box = builder.build_bounding_box(xor_gate, num_dashes=60)

        self.wait(3)

        # 외부 와이어 생성
        input_wires, input_points = self._create_input_wires(plane, xor_gate)
        output_wire, output_point = self._create_output_wire(plane, xor_gate)

        # 라벨 생성
        labels = VGroup(
            plane.create_label("A", input_points[0], offset=LEFT * 0.5),
            plane.create_label("B", input_points[1], offset=LEFT * 0.5),
            plane.create_label("Y", output_point, offset=RIGHT * 0.5)
        )

        # 애니메이션
        self.play(
            Create(VGroup(*input_wires, output_wire)),
            Write(labels)
        )
        self.wait(3)

    def _create_input_wires(self, plane: BreadBoardPlane, gate: CompositeGate) -> tuple[list[Wire], list[tuple]]:
        """입력 와이어 생성"""
        input_coords = {
            'a': {'port': 'input_a', 'offset': -1.5},
            'b': {'port': 'input_b', 'offset': -1.5}
        }

        wires = []
        start_points = []
        for port_name, info in input_coords.items():
            end_point = gate.get_port_by_name(info['port']).get_center()
            start_point = (
                end_point[0] + info['offset'],
                end_point[1],
            )
            wire = plane.create_wire(end_point, start_point)
            wires.append(wire)
            start_points.append(start_point)

        return wires, start_points

    def _create_output_wire(self, plane: BreadBoardPlane, gate: CompositeGate) -> tuple[Wire, tuple]:
        """출력 와이어 생성"""
        start_point = gate.get_port_by_name('output').get_center()
        end_point = (
            start_point[0] + 1.5,
            start_point[1],
        )
        wire = plane.create_wire(start_point, end_point)
        return wire, end_point
