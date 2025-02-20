from manim import *
from common.logic_gate.logic_gate import LogicGate
from common.logic_gate.composite_gate import CompositeGate
from common.logic_gate.styles import LogicGateStyle


class CompositeGateBuilder:
    """복합 게이트 빌더"""

    def __init__(self, bread_board):
        self.board = bread_board

    def build_half_adder(self, pos: tuple[float, float], **kwargs) -> CompositeGate:
        """반가산기 생성
        Returns:
            CompositeGate: 입출력 포트가 노출된 반가산기
        """
        composite = CompositeGate(**kwargs)
        base_x, base_y = pos
        spacing = LogicGateStyle.COMPOSITE_GATE_SPACING

        # 내부 게이트 생성 및 배치
        xor_gate = self.board.create_xor_gate(
            (base_x, base_y + spacing/2), **kwargs)
        and_gate = self.board.create_and_gate(
            (base_x, base_y - spacing/2), **kwargs)

        # 게이트를 컴포짓에 추가
        composite.add_internal_gate(xor_gate)
        composite.add_internal_gate(and_gate)

        # 외부 포트 생성 및 매핑

        x_offset = 1.5
        input_a_y = self.board.get_gate_input_coords(xor_gate, 0)[1]
        input_b_y = self.board.get_gate_input_coords(xor_gate, 1)[1]
        output_sum_y = self.board.get_gate_output_coords(xor_gate)[1]
        output_carry_y = self.board.get_gate_output_coords(and_gate)[1]

        input_a = composite._create_port(
            self.board.c2p(base_x - x_offset, input_a_y))
        input_b = composite._create_port(
            self.board.c2p(base_x - x_offset, input_b_y))

        output_sum = composite._create_port(
            self.board.c2p(base_x + x_offset, output_sum_y))
        output_carry = composite._create_port(
            self.board.c2p(base_x + x_offset, output_carry_y))

        # 포트 매핑
        composite.map_external_port('input_a', input_a)
        composite.map_external_port('input_b', input_b)
        composite.map_external_port('output_sum', output_sum)
        composite.map_external_port('output_carry', output_carry)

        # 내부 와이어 연결
        wires = [
            # input_a에서 분기
            self.board.create_wire(input_a.get_center(),
                                   xor_gate.input_ports[0].get_center()),
            # input_a에서 and_gate로의 꺾인 와이어
            self.board.create_wire(
                input_a.get_center() + RIGHT * 0.7,
                and_gate.input_ports[0].get_center(),
                mid_points=[np.array([
                    input_a.get_center()[0] + 0.7,  # x 좌표
                    and_gate.input_ports[0].get_center()[1],  # y 좌표
                    0  # z 좌표
                ])]
            ),

            # input_b에서 분기
            self.board.create_wire(input_b.get_center(),
                                   xor_gate.input_ports[1].get_center()),

            self.board.create_wire(
                input_b.get_center() + RIGHT * 0.3,
                and_gate.input_ports[1].get_center(),
                mid_points=[np.array([
                    input_b.get_center()[0] + 0.3,  # x 좌표
                    and_gate.input_ports[1].get_center()[1],  # y 좌표
                    0  # z 좌표
                ])]
            ),

            # 출력 연결
            self.board.create_wire(
                xor_gate.output_ports[0].get_center(), output_sum.get_center()),
            self.board.create_wire(
                and_gate.output_ports[0].get_center(), output_carry.get_center())
        ]

        # 와이어 추가 및 연결
        for wire in wires:
            composite.add_internal_wire(wire)

        return composite

    def build_nand_xor(self, pos: tuple[float, float], **kwargs) -> CompositeGate:
        """NAND 게이트들로 구성된 XOR 게이트 생성"""
        composite = CompositeGate(**kwargs)
        base_x, base_y = pos
        spacing = LogicGateStyle.COMPOSITE_GATE_SPACING * 0.6

        # NAND 게이트들 생성 및 배치
        nand1 = self.board.create_nand_gate(
            (base_x - spacing * 3, 0),
            **kwargs
        )

        nand2 = self.board.create_nand_gate(
            (base_x, base_y + spacing * 2),
            **kwargs
        )

        nand3 = self.board.create_nand_gate(
            (base_x, base_y - spacing * 2),
            **kwargs
        )

        nand4 = self.board.create_nand_gate(
            # 우하단: x방향 2.5배, y방향 -spacing/2
            (base_x + spacing * 3, 0),
            **kwargs
        )

        # 게이트들을 컴포짓에 추가
        for gate in [nand1, nand2, nand3, nand4]:
            composite.add_internal_gate(gate)

        # 외부 포트 생성
        x_offset = spacing * 5

        input_a_x = base_x - x_offset
        input_a_y = nand2.get_input_point(0)[1]
        input_a = composite._create_port(self.board.c2p(input_a_x, input_a_y))

        input_b_x = base_x - x_offset
        input_b_y = nand3.get_input_point(1)[1]
        input_b = composite._create_port(self.board.c2p(input_b_x, input_b_y))

        output = composite._create_port(
            self.board.c2p(base_x + x_offset, base_y)
        )

        # 포트 매핑
        composite.map_external_port('input_a', input_a)
        composite.map_external_port('input_b', input_b)
        composite.map_external_port('output', output)

        # 내부 와이어 연결
        wires = [
            # 입력 A 분기
            self.board.create_wire(
                input_a.get_center(),
                nand2.input_ports[0].get_center()
            ),
            self.board.create_wire(
                input_a.get_center(),
                nand1.input_ports[0].get_center(),
                mid_points=[
                    np.array([
                        input_a.get_center()[0] + spacing / 2,
                        input_a.get_center()[1],
                        0
                    ]),
                    np.array([
                        input_a.get_center()[0] + spacing / 2,
                        nand1.input_ports[0].get_center()[1],
                        0
                    ])
                ]
            ),

            # 입력 B 분기
            self.board.create_wire(
                input_b.get_center(),
                nand1.input_ports[1].get_center(),
                mid_points=[
                    np.array([
                        input_b.get_center()[0] + spacing / 2,
                        input_b.get_center()[1],
                        0
                    ]),
                    np.array([
                        input_b.get_center()[0] + spacing / 2,
                        nand1.input_ports[1].get_center()[1],
                        0
                    ])
                ]
            ),
            self.board.create_wire(
                input_b.get_center(),
                nand3.input_ports[1].get_center()
            ),

            # NAND1 출력 -> NAND2 입력
            self.board.create_wire(
                nand1.output_ports[0].get_center(),
                nand2.input_ports[1].get_center(),
                mid_points=[
                    np.array([
                        nand1.output_ports[0].get_center()[0] + spacing / 2,
                        nand1.output_ports[0].get_center()[1],
                        0
                    ]),
                    np.array([
                        nand1.output_ports[0].get_center()[0] + spacing / 2,
                        nand2.input_ports[1].get_center()[1],
                        0
                    ])
                ]
            ),

            # NAND1 출력 -> NAND3 입력
            self.board.create_wire(
                nand1.output_ports[0].get_center(),
                nand3.input_ports[0].get_center(),
                mid_points=[
                    np.array([
                        nand1.output_ports[0].get_center()[0] + spacing / 2,
                        nand1.output_ports[0].get_center()[1],
                        0
                    ]),
                    np.array([
                        nand1.output_ports[0].get_center()[0] + spacing / 2,
                        nand3.input_ports[0].get_center()[1],
                        0
                    ])
                ]
            ),

            # NAND2 출력 -> NAND4 입력 1
            self.board.create_wire(
                nand2.output_ports[0].get_center(),
                nand4.input_ports[0].get_center(),
                mid_points=[
                    np.array([
                        nand2.output_ports[0].get_center()[0] + spacing / 2,
                        nand2.output_ports[0].get_center()[1],
                        0
                    ]),
                    np.array([
                        nand2.output_ports[0].get_center()[0] + spacing / 2,
                        nand4.input_ports[0].get_center()[1],
                        0
                    ])
                ]
            ),

            # NAND3 출력 -> NAND4 입력 2
            self.board.create_wire(
                nand3.output_ports[0].get_center(),
                nand4.input_ports[1].get_center(),
                mid_points=[
                    np.array([
                        nand3.output_ports[0].get_center()[0] + spacing / 2,
                        nand3.output_ports[0].get_center()[1],
                        0
                    ]),
                    np.array([
                        nand3.output_ports[0].get_center()[0] + spacing / 2,
                        nand4.input_ports[1].get_center()[1],
                        0
                    ])
                ]
            ),

            # NAND4 출력
            self.board.create_wire(
                nand4.output_ports[0].get_center(), output.get_center())
        ]

        # 와이어 추가
        for wire in wires:
            composite.add_internal_wire(wire)

        return composite

    def build_bounding_box(self,
                           gate: LogicGate,
                           padding: float = LogicGateStyle.COMPOSITE_GATE_BOX_PADDING,
                           stroke_color: str = LogicGateStyle.COMPOSITE_GATE_BOX_COLOR,
                           stroke_width: float = LogicGateStyle.COMPOSITE_GATE_BOX_STROKE_WIDTH,
                           stroke_opacity: float = LogicGateStyle.COMPOSITE_GATE_BOX_STROKE_OPACITY,
                           as_dashed: bool = True,
                           num_dashes: int = LogicGateStyle.COMPOSITE_GATE_BOX_DASH_NUM,
                           dashed_ratio: float = LogicGateStyle.COMPOSITE_GATE_BOX_DASH_RATIO
                           ) -> Rectangle:
        """복합 게이트의 바운딩 박스 생성

        Args:
            gate: 바운딩 박스를 생성할 논리 게이트
            padding: 게이트와의 여백 (게이트 크기 대비 비율)
            stroke_color: 박스 선 색상
            stroke_width: 박스 선 두께
            stroke_opacity: 박스 선 투명도
            as_dashed: 점선 여부
        """
        # 게이트 자체가 이미 VGroup이므로 별도 그룹화 불필요
        padding_amount = gate.size * padding
        box = Rectangle(
            width=gate.width + padding_amount * 2,
            height=gate.height + padding_amount * 2,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity
        ).move_to(gate.get_center())

        if as_dashed:
            box = DashedVMobject(box, num_dashes=num_dashes,
                                 dashed_ratio=dashed_ratio)

        self.board.add(box)
        return box
