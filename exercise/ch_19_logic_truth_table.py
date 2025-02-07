from manim import *
from typing import List, Any


class TruthTable(Table):
    # 스타일 관련 상수
    FONT_SIZE = 62
    LABEL_COLOR = YELLOW
    SOURCE_COLOR = GREEN
    RESULT_COLOR = PINK
    LINE_COLOR = BLUE_B
    LINE_STROKE_WIDTH = 1

    # 간격 조정 상수
    HEADER_LINE_SHIFT = 0.05
    VERTICAL_LINE_SHIFT = 0.05

    def __init__(self,
                 table_data: List[List[str]],
                 col_labels: List[str],
                 source_vars_count: int = 1,  # 소스 논리 변수 개수
                 **kwargs: Any) -> None:
        super().__init__(
            table_data,
            col_labels=[MathTex(label, font_size=self.FONT_SIZE)
                        for label in col_labels],
            include_outer_lines=True,
            line_config={"color": self.LINE_COLOR,
                         "stroke_width": self.LINE_STROKE_WIDTH},
            **kwargs
        )

        self.source_vars_count = source_vars_count
        self._style_table()
        self._add_double_lines()

    def _style_table(self) -> None:
        self.get_labels().set_color(self.LABEL_COLOR)
        for row in self.get_rows()[1:]:
            # 소스 변수 컬럼들의 텍스트를 녹색으로 설정
            for i in range(self.source_vars_count):
                row[i].set_color(self.SOURCE_COLOR)
            # 결과 컬럼의 텍스트를 분홍색으로 설정
            row[self.source_vars_count:].set_color(self.RESULT_COLOR)

    def _add_double_lines(self) -> None:
        # 헤더 이중선
        second_h_line = self.get_horizontal_lines()[2]
        self.second_h_line_copy = second_h_line.copy().shift(UP * self.HEADER_LINE_SHIFT)

        # 소스 변수들과 결과를 구분하는 수직 이중선
        v_lines = self.get_vertical_lines()
        self.v_line_copies = []

        # 소스 변수 개수에 따라 수직 구분선 위치 결정
        divider_index = self.source_vars_count + 1
        source_divider_v_line = v_lines[divider_index]
        v_line_copy = source_divider_v_line.copy().shift(LEFT * self.VERTICAL_LINE_SHIFT)
        self.v_line_copies.append(v_line_copy)

    def get_table_group(self) -> VGroup:
        return VGroup(
            self,
            self.second_h_line_copy,
            *self.v_line_copies
        )


class LogicTruthTable(Scene):
    # 스타일 관련 상수
    TITLE_FONT_SIZE = 82
    TITLE_COLOR = YELLOW
    TABLE_VERTICAL_OFFSET = 1.1
    TITLE_VERTICAL_SHIFT = 0.1

    # 애니메이션 관련 상수
    FADE_TIME = 1.0
    WAIT_TIME = 2.0

    def create_section(self,
                       section_number: int,
                       title_expr: str,
                       table_data: List[List[str]],
                       col_labels: List[str],
                       source_vars_count: int = 1) -> VGroup:
        # 섹션 타이틀 생성
        title = MathTex(
            f"\\text{{{section_number}. }} {title_expr}",
            font_size=self.TITLE_FONT_SIZE,
            color=self.TITLE_COLOR
        ).to_corner(UL).shift(UP * self.TITLE_VERTICAL_SHIFT)

        # 진리표 생성
        truth_table = TruthTable(
            table_data=table_data,
            col_labels=col_labels,
            source_vars_count=source_vars_count
        )
        truth_table_group = truth_table.get_table_group()
        truth_table_group.align_to(title, UP).shift(
            DOWN * self.TABLE_VERTICAL_OFFSET)

        return VGroup(title, truth_table_group)

    def _generate_truth_pattern(self) -> List[List[str]]:
        """2변수 진리표의 기본 패턴 생성"""
        return [
            ["0", "0"],
            ["0", "1"],
            ["1", "0"],
            ["1", "1"]
        ]

    def _get_pattern_name(self, output_pattern: List[str]) -> tuple[str, str, str]:
        """출력 패턴에 따른 (타이틀 수식, 설명, 열 레이블) 반환"""
        pattern_map = {
            # 상수
            "0000": (r"0", "contradiction", r"0"),
            "1111": (r"1", "tautology", r"1"),

            # 기본 연산자
            "0001": (r"p \land q", "conjunction", r"p \land q"),
            "0111": (r"p \lor q", "disjunction", r"p \lor q"),
            "0110": (r"p \oplus q", "exclusive or, XOR", r"p \oplus q"),

            # 부정 연산자 조합
            "1000": (r"\neg(p \lor q)", "NOR", r"\neg(p \lor q)"),
            "1110": (r"\neg(p \land q)", "NAND", r"\neg(p \land q)"),

            # 단항 연산자
            "0011": (r"p", "projection of p", r"p"),
            "0101": (r"q", "projection of q", r"q"),
            "1100": (r"\neg p", "", r"\neg p"),
            "1010": (r"\neg q", "", r"\neg q"),

            # 이항 연산자와 부정의 조합
            "0010": (r"p \land \neg q", "", r"p \land \neg q"),
            "0100": (r"\neg p \land q", "", r"\neg p \land q"),
            "1011": (r"p \lor \neg q", "", r"p \lor \neg q"),

            # 동치 관계
            "1001": (r"p \leftrightarrow q", "equivalence", r"p \leftrightarrow q"),
            "1101": (r"\neg p \lor q", r"\text{equivalent to }p \rightarrow q", r"\neg p \lor q"),
        }
        return pattern_map.get("".join(output_pattern))

    def construct(self):
        # 첫 번째 섹션: 부정 연산
        self.next_section("truth table for: ~p")
        negation_section = self.create_section(
            section_number=1,
            title_expr=r"\neg p \text{ (negation)}",
            table_data=[
                ["0", "1"],
                ["1", "0"]
            ],
            col_labels=["p", r"\neg p"],
            source_vars_count=1
        )
        self.play(FadeIn(negation_section), run_time=self.FADE_TIME)
        self.wait(self.WAIT_TIME)
        self.play(FadeOut(negation_section), run_time=self.FADE_TIME)

        self.next_section("truth table for: p, q")
        # 2변수 진리표들 (16가지 패턴)
        base_pattern = self._generate_truth_pattern()
        prev_section = None

        for pattern_num in range(16):
            self.next_section(f"truth table pattern {pattern_num + 1}")

            if prev_section:
                self.play(FadeOut(prev_section), run_time=self.FADE_TIME)

            # 4비트 이진수로 변환하여 출력 패턴 생성
            output_bits = format(pattern_num, '04b')
            output_pattern = list(output_bits)
            expr, name, col_label = self._get_pattern_name(output_pattern)

            # 진리표 데이터 생성
            table_data = [
                row + [out] for row, out in zip(base_pattern, output_pattern)
            ]

            # 설명이 있는 경우에만 괄호를 포함하고, 적절한 공백 추가
            if not name:
                title_expr = expr
            else:
                title_expr = (f"{expr} \\text{{ \\,({name})\\,}}"
                              if not name.startswith(r"\text{")
                              else f"{expr} \\,({name})\\,")

            section = self.create_section(
                section_number=pattern_num + 2,  # 부정 연산이 1번이므로 2번부터 시작
                title_expr=title_expr,
                table_data=table_data,
                col_labels=["p", "q", col_label],
                source_vars_count=2
            )

            self.play(FadeIn(section), run_time=self.FADE_TIME)
            prev_section = section
            self.wait(self.WAIT_TIME)

        self.wait(self.WAIT_TIME)
