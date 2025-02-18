from manim import *
from typing import List, Any, Tuple, Union


class PropositionalLogicTable(Table):
    # 스타일 관련 상수
    FONT_SIZE = 62  # FONT_SIZE 증가
    TITLE_FONT_SIZE = 72
    PREMISE_COLOR = GREEN
    INTERMEDIATE_COLOR = YELLOW  # 중간 단계 색상 추가
    CONCLUSION_COLOR = PINK
    STEP_NUMBER_COLOR = BLUE_A  # 단계 번호 색상 추가
    LINE_COLOR = BLUE_B
    LINE_STROKE_WIDTH = 1
    TABLE_SCALE = 0.8

    # 테이블 데이터 관련 상수 추가
    STEP_NUMBER_SUFFIX = "."        # 단계 번호 뒤의 구분자
    EMPTY_CELL = ""                 # 빈 셀 표현
    OPERATOR_SPACES = r"\ \ "       # 연산자 앞뒤 공백

    @classmethod
    def make_step_number(cls, num: int) -> str:
        """단계 번호 문자열 생성"""
        return f"{num}{cls.STEP_NUMBER_SUFFIX}" if num > 0 else cls.EMPTY_CELL

    @classmethod
    def add_operator_spaces(cls, expr: str) -> str:
        """연산자 앞뒤에 공백 추가"""
        return f"{cls.OPERATOR_SPACES}{expr}{cls.OPERATOR_SPACES}"

    def __init__(self,
                 table_data: List[List[str]],
                 last_premise_index: int = 0,  # 마지막 전제의 인덱스
                 **kwargs: Any) -> None:
        super().__init__(
            table_data,
            include_outer_lines=False,
            line_config={"color": self.LINE_COLOR,
                         "stroke_width": self.LINE_STROKE_WIDTH},
            element_to_mobject=MathTex,
            element_to_mobject_config={"font_size": self.FONT_SIZE},
            **kwargs
        )
        self.last_premise_index = last_premise_index
        self._style_table()

    def _style_table(self) -> None:
        # 수평선 처리
        h_lines = self.get_horizontal_lines()
        h_lines.set_opacity(0)

        # 마지막 전제 다음에 구분선 표시
        if self.last_premise_index >= 0:
            h_lines[self.last_premise_index].set_opacity(1)

        # 결론 구분선
        h_lines[-1].set_opacity(1)

        # 가정과 결론 색상 처리
        rows = self.get_rows()

        # 단계 번호(1열) 색상 처리
        for row in rows:
            if row[0].tex_string.strip():  # 빈 문자열이 아닌 경우만
                row[0].set_color(self.STEP_NUMBER_COLOR)

        # 모든 전제를 녹색으로
        for i in range(self.last_premise_index + 1):
            if rows[i][1].tex_string.strip():  # 빈 줄이 아닌 경우만
                rows[i][1].set_color(self.PREMISE_COLOR)

        # 중간 단계를 노란색으로
        for i in range(self.last_premise_index + 1, len(rows) - 1):
            if rows[i][1].tex_string.strip():  # 빈 줄이 아닌 경우만
                rows[i][1].set_color(self.INTERMEDIATE_COLOR)

        # 결론을 분홍색으로
        rows[-1][1].set_color(self.CONCLUSION_COLOR)


class PropositionalLogic10BasicRules(Scene):
    # 규칙 타이틀 관련 상수
    TITLE_PREFIX = r"\text"         # \text 매크로
    TITLE_SEPARATOR = ". "          # 번호와 규칙명 사이 구분자
    TITLE_BRACKET_OPEN = "("
    TITLE_BRACKET_CLOSE = ")"

    # 논리연산자 상수 통합 및 재조직화
    class LogicRules:
        class Operators:
            NEGATION = r"\sim"
            CONJUNCTION = r"\&"
            DISJUNCTION = r"\vee"
            CONDITIONAL = r"\rightarrow"
            BICONDITIONAL = r"\leftrightarrow"

        class Types:
            INTRO = "Intro"     # 괄호 안에서만 사용될 줄임말
            ELIM = "Elim"       # 괄호 안에서만 사용될 줄임말

        class Names:
            NEGATION = "Negation"
            CONJUNCTION = "Conjunction"
            DISJUNCTION = "Disjunction"
            CONDITIONAL = "Implication"
            BICONDITIONAL = "Biconditional"

        class FullNames:        # 규칙 이름에서 사용될 전체 단어
            INTRODUCTION = "Introduction"
            ELIMINATION = "Elimination"

        @classmethod
        def make_rule_name(cls, base_name: str, type_name: str) -> str:
            # type_name에 따라 전체 이름 사용
            full_type = (cls.FullNames.INTRODUCTION if type_name == cls.Types.INTRO
                         else cls.FullNames.ELIMINATION)
            return f"{base_name} {full_type}"

    # 규칙명 관련 상수 재정의
    RULE_NEGATION_INTRO = LogicRules.make_rule_name(
        LogicRules.Names.NEGATION, LogicRules.Types.INTRO)
    RULE_NEGATION_ELIM = LogicRules.make_rule_name(
        LogicRules.Names.NEGATION, LogicRules.Types.ELIM)
    RULE_CONJUNCTION_INTRO = LogicRules.make_rule_name(
        LogicRules.Names.CONJUNCTION, LogicRules.Types.INTRO)
    RULE_CONJUNCTION_ELIM = LogicRules.make_rule_name(
        LogicRules.Names.CONJUNCTION, LogicRules.Types.ELIM)
    RULE_DISJUNCTION_INTRO = LogicRules.make_rule_name(
        LogicRules.Names.DISJUNCTION, LogicRules.Types.INTRO)
    RULE_DISJUNCTION_ELIM = LogicRules.make_rule_name(
        LogicRules.Names.DISJUNCTION, LogicRules.Types.ELIM)
    RULE_IMPLICATION_INTRO = LogicRules.make_rule_name(
        LogicRules.Names.CONDITIONAL, LogicRules.Types.INTRO)
    RULE_IMPLICATION_ELIM = LogicRules.make_rule_name(
        LogicRules.Names.CONDITIONAL, LogicRules.Types.ELIM)
    RULE_BICONDITIONAL_INTRO = LogicRules.make_rule_name(
        LogicRules.Names.BICONDITIONAL, LogicRules.Types.INTRO)
    RULE_BICONDITIONAL_ELIM = LogicRules.make_rule_name(
        LogicRules.Names.BICONDITIONAL, LogicRules.Types.ELIM)

    # 규칙 기호 상수 재정의
    RULE_SYMBOL_NEGATION = LogicRules.Operators.NEGATION
    RULE_SYMBOL_CONJUNCTION = LogicRules.Operators.CONJUNCTION
    RULE_SYMBOL_DISJUNCTION = LogicRules.Operators.DISJUNCTION
    RULE_SYMBOL_IMPLICATION = LogicRules.Operators.CONDITIONAL
    RULE_SYMBOL_BICONDITIONAL = LogicRules.Operators.BICONDITIONAL

    # 섹션 번호 상수
    SECTION_NEGATION_INTRO = 1
    SECTION_NEGATION_ELIM = 2
    SECTION_CONJUNCTION_INTRO = 3
    SECTION_CONJUNCTION_ELIM = 4
    SECTION_DISJUNCTION_INTRO = 5
    SECTION_DISJUNCTION_ELIM = 6
    SECTION_IMPLICATION_INTRO = 7
    SECTION_IMPLICATION_ELIM = 8
    SECTION_BICONDITIONAL_INTRO = 9
    SECTION_BICONDITIONAL_ELIM = 10

    # 버퍼 관련 상수
    BUFF_DEFAULT = 0.25
    BUFF_MEDIUM = 0.75      # 중간 테이블용 버퍼
    BUFF_LARGE = 1.75       # 작은 테이블용 큰 버퍼

    # 테이블 크기와 버퍼값 매핑
    class TableSizes:
        LARGE = "large"      # 큰 테이블 (부정 도입)
        MEDIUM = "medium"    # 중간 테이블 (조건문 도입)
        SMALL = "small"      # 작은 테이블 (나머지)

    # 테이블 크기별 버퍼값 매핑
    BUFF_BY_SIZE = {
        TableSizes.LARGE: BUFF_DEFAULT,
        TableSizes.MEDIUM: BUFF_MEDIUM,
        TableSizes.SMALL: BUFF_LARGE
    }

    # 애니메이션 타이밍 관련 상수
    FADE_IN_TIME = 1.0
    FADE_OUT_TIME = 1.0
    WAIT_TIME = 2.0

    # 테이블 간격 상수 추가
    TABLE_SPACING = 1.0  # 테이블 사이의 간격

    # 타이틀 위치 관련 상수 수정
    TITLE_TOP_MARGIN = 0.5  # 1.5에서 0.5로 수정하여 타이틀을 위로 올림

    def create_section_title(self,
                             section_num: int,          # 먼저 필수 파라미터
                             rule_name: str,
                             rule_symbol: str,
                             rule_type: str = None  # 기본값을 None으로
                             ) -> MathTex:
        """섹션 타이틀 생성"""
        if rule_type is None:
            rule_type = self.LogicRules.Types.INTRO  # 클래스 내부에서 참조

        return MathTex(
            f"{self.TITLE_PREFIX}{{{section_num}{self.TITLE_SEPARATOR}{rule_name} }}"
            f" {self.TITLE_BRACKET_OPEN}{rule_symbol}\\ {self.TITLE_PREFIX}{{{rule_type}}}{self.TITLE_BRACKET_CLOSE}",
            font_size=PropositionalLogicTable.TITLE_FONT_SIZE,
            color=YELLOW  # 타이틀 색상을 YELLOW로 변경
        ).to_edge(UP, buff=self.TITLE_TOP_MARGIN)

    def animate_section(self, title: MathTex,
                        table_or_group: Union[PropositionalLogicTable, VGroup]
                        ) -> Tuple[MathTex, Union[PropositionalLogicTable, VGroup]]:
        """섹션 애니메이션 실행 및 생성된 객체 반환"""
        self.play(FadeIn(title), run_time=self.FADE_IN_TIME)
        self.play(FadeIn(table_or_group), run_time=self.FADE_IN_TIME)
        self.wait(self.WAIT_TIME)
        return title, table_or_group

    def position_content(self, title: MathTex,
                         table_or_group: Union[PropositionalLogicTable, VGroup],
                         buff: float) -> None:
        """타이틀과 테이블 위치 조정을 위한 통합 메서드"""
        # 1. 타이틀을 항상 동일한 위치에 배치
        title.to_edge(UP, buff=self.TITLE_TOP_MARGIN)

        # 2. 테이블/그룹을 수평 중앙에 배치하되 수직 위치는 유지
        current_y = table_or_group.get_center()[1]  # 현재 y 위치 저장
        table_or_group.move_to([0, current_y, 0])   # x만 중앙으로

        # 3. 테이블/그룹의 수직 위치를 타이틀 기준으로 조정
        table_or_group.next_to(title, DOWN, buff=buff)

    def create_negation_intro_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, PropositionalLogicTable]:
        """부정 도입 규칙의 타이틀과 테이블을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_NEGATION_INTRO,
            rule_name=self.RULE_NEGATION_INTRO,
            rule_symbol=self.RULE_SYMBOL_NEGATION
            # rule_type 기본값 사용
        )

        table_data = [
            [PropositionalLogicTable.make_step_number(1), "P"],
            [PropositionalLogicTable.make_step_number(2),
                PropositionalLogicTable.EMPTY_CELL],
            [PropositionalLogicTable.make_step_number(3),
                PropositionalLogicTable.EMPTY_CELL],
            [PropositionalLogicTable.EMPTY_CELL, "Q"],
            [PropositionalLogicTable.EMPTY_CELL, r"\sim Q"],
            [PropositionalLogicTable.EMPTY_CELL, r"\sim P"]
        ]

        table = PropositionalLogicTable(
            table_data,
            last_premise_index=0    # P가 유일한 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        self.position_content(title, table, buff)

        return title, table

    def create_negation_elim_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, PropositionalLogicTable]:
        """부정 제거 규칙의 타이틀과 테이블을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_NEGATION_ELIM,
            rule_name=self.RULE_NEGATION_ELIM,
            rule_symbol=self.RULE_SYMBOL_NEGATION,
            rule_type=self.LogicRules.Types.ELIM  # 명시적으로 Types.ELIM 지정
        )

        table_data = [
            [PropositionalLogicTable.make_step_number(1),
                r"\sim \sim P"],  # 이중 부정
            [PropositionalLogicTable.EMPTY_CELL, "P"]                # 결론
        ]

        table = PropositionalLogicTable(
            table_data,
            last_premise_index=0     # 첫 번째 행이 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        self.position_content(title, table, buff)

        return title, table

    def create_conjunction_intro_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, PropositionalLogicTable]:
        """논리곱 도입 규칙의 타이틀과 테이블을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_CONJUNCTION_INTRO,
            rule_name=self.RULE_CONJUNCTION_INTRO,
            rule_symbol=self.RULE_SYMBOL_CONJUNCTION
        )

        table_data = [
            [PropositionalLogicTable.make_step_number(1), "P"],
            [PropositionalLogicTable.make_step_number(2), "Q"],
            [PropositionalLogicTable.EMPTY_CELL,
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.CONJUNCTION)}Q"]
        ]

        table = PropositionalLogicTable(
            table_data,
            last_premise_index=1    # P, Q 모두가 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        self.position_content(title, table, buff)

        return title, table

    def create_conjunction_elim_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, VGroup]:
        """논리곱 제거 규칙의 타이틀과 테이블들을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_CONJUNCTION_ELIM,
            rule_name=self.RULE_CONJUNCTION_ELIM,
            rule_symbol=self.RULE_SYMBOL_CONJUNCTION,
            rule_type=self.LogicRules.Types.ELIM  # 명시적으로 Types.ELIM 지정
        )

        # 첫 번째 테이블 (P & Q ⊢ P)
        left_table_data = [
            [PropositionalLogicTable.make_step_number(1), "P\\ \&\\ Q"],
            [PropositionalLogicTable.EMPTY_CELL, "P"]
        ]

        # 두 번째 테이블 (P & Q ⊢ Q)
        right_table_data = [
            [PropositionalLogicTable.make_step_number(1), "P\\ \&\\ Q"],
            [PropositionalLogicTable.EMPTY_CELL, "Q"]
        ]

        # 두 테이블 생성
        left_table = PropositionalLogicTable(
            left_table_data,
            last_premise_index=0
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        right_table = PropositionalLogicTable(
            right_table_data,
            last_premise_index=0
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        # 두 테이블을 그룹으로 묶고 수평 정렬
        tables = VGroup(left_table, right_table).arrange(
            RIGHT, buff=self.TABLE_SPACING)

        self.position_content(title, tables, buff)

        return title, tables

    def create_disjunction_intro_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, VGroup]:
        """선언 도입 규칙의 타이틀과 테이블들을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_DISJUNCTION_INTRO,
            rule_name=self.RULE_DISJUNCTION_INTRO,
            rule_symbol=self.RULE_SYMBOL_DISJUNCTION,
            rule_type=self.LogicRules.Types.INTRO
        )

        # 첫 번째 테이블 (P ⊢ P ∨ Q)
        left_table_data = [
            [PropositionalLogicTable.make_step_number(1), "P"],
            [PropositionalLogicTable.EMPTY_CELL,
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.DISJUNCTION)}Q"]
        ]

        # 두 번째 테이블 (Q ⊢ Q ∨ P)
        right_table_data = [
            [PropositionalLogicTable.make_step_number(1), "Q"],
            [PropositionalLogicTable.EMPTY_CELL,
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.DISJUNCTION)}Q"]
        ]

        # 두 테이블 생성
        left_table = PropositionalLogicTable(
            left_table_data,
            last_premise_index=0
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        right_table = PropositionalLogicTable(
            right_table_data,
            last_premise_index=0
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        # 두 테이블을 그룹으로 묶고 수평 정렬
        tables = VGroup(left_table, right_table).arrange(
            RIGHT, buff=self.TABLE_SPACING)

        self.position_content(title, tables, buff)

        return title, tables

    def create_disjunction_elim_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, VGroup]:
        """선언 제거 규칙의 타이틀과 테이블들을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_DISJUNCTION_ELIM,
            rule_name=self.RULE_DISJUNCTION_ELIM,
            rule_symbol=self.RULE_SYMBOL_DISJUNCTION,
            rule_type=self.LogicRules.Types.ELIM
        )

        # 첫 번째 테이블 (P ∨ Q, ~P ⊢ Q)
        left_table_data = [
            [PropositionalLogicTable.make_step_number(1), "P\\ \\vee\\ Q"],
            [PropositionalLogicTable.make_step_number(2), r"\sim P"],
            [PropositionalLogicTable.EMPTY_CELL, "Q"]
        ]

        # 두 번째 테이블 (P ∨ Q, ~Q ⊢ P)
        right_table_data = [
            [PropositionalLogicTable.make_step_number(1), "P\\ \\vee\\ Q"],
            [PropositionalLogicTable.make_step_number(2), r"\sim Q"],
            [PropositionalLogicTable.EMPTY_CELL, "P"]
        ]

        # 두 테이블 생성
        left_table = PropositionalLogicTable(
            left_table_data,
            last_premise_index=1    # 첫 두 행이 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        right_table = PropositionalLogicTable(
            right_table_data,
            last_premise_index=1    # 첫 두 행이 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        # 두 테이블을 그룹으로 묶고 수평 정렬
        tables = VGroup(left_table, right_table).arrange(
            RIGHT, buff=self.TABLE_SPACING)

        self.position_content(title, tables, buff)

        return title, tables

    def create_implication_intro_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, PropositionalLogicTable]:
        """조건문 도입 규칙의 타이틀과 테이블을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_IMPLICATION_INTRO,
            rule_name=self.RULE_IMPLICATION_INTRO,
            rule_symbol=self.RULE_SYMBOL_IMPLICATION
        )

        table_data = [
            [PropositionalLogicTable.make_step_number(1), "P"],            # 전제
            [PropositionalLogicTable.make_step_number(2),
                PropositionalLogicTable.EMPTY_CELL],    # 빈 중간단계
            [PropositionalLogicTable.make_step_number(3),
                PropositionalLogicTable.EMPTY_CELL],    # 빈 중간단계
            [PropositionalLogicTable.EMPTY_CELL, "Q"],                     # 보조 결론
            [PropositionalLogicTable.EMPTY_CELL,
                # 최종 결론
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.CONDITIONAL)}Q"]
        ]

        table = PropositionalLogicTable(
            table_data,
            last_premise_index=0    # P가 유일한 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        self.position_content(title, table, buff)
        return title, table

    def create_implication_elim_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, PropositionalLogicTable]:
        """조건문 제거 규칙의 타이틀과 테이블을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_IMPLICATION_ELIM,
            rule_name=self.RULE_IMPLICATION_ELIM,
            rule_symbol=self.RULE_SYMBOL_IMPLICATION,
            rule_type=self.LogicRules.Types.ELIM  # 명시적으로 Types.ELIM 지정
        )

        table_data = [
            [PropositionalLogicTable.make_step_number(1),
                # 첫 번째 전제
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.CONDITIONAL)}Q"],
            [PropositionalLogicTable.make_step_number(2), "P"],    # 두 번째 전제
            [PropositionalLogicTable.EMPTY_CELL, "Q"]             # 결론
        ]

        table = PropositionalLogicTable(
            table_data,
            last_premise_index=1    # 첫 두 행이 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        self.position_content(title, table, buff)
        return title, table

    def create_biconditional_intro_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, PropositionalLogicTable]:
        """쌍조건문 도입 규칙의 타이틀과 테이블을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_BICONDITIONAL_INTRO,
            rule_name=self.RULE_BICONDITIONAL_INTRO,
            rule_symbol=self.RULE_SYMBOL_BICONDITIONAL
        )

        table_data = [
            [PropositionalLogicTable.make_step_number(1),
                # 첫 번째 전제
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.CONDITIONAL)}Q"],
            [PropositionalLogicTable.make_step_number(2),
                # 두 번째 전제
                f"Q{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.CONDITIONAL)}P"],
            [PropositionalLogicTable.EMPTY_CELL,
                # 결론
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.BICONDITIONAL)}Q"]
        ]

        table = PropositionalLogicTable(
            table_data,
            last_premise_index=1    # 첫 두 행이 전제
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        self.position_content(title, table, buff)
        return title, table

    def create_biconditional_elim_section(self, buff: float = BUFF_DEFAULT) -> Tuple[MathTex, VGroup]:
        """쌍조건문 제거 규칙의 타이틀과 테이블들을 생성"""
        title = self.create_section_title(
            section_num=self.SECTION_BICONDITIONAL_ELIM,
            rule_name=self.RULE_BICONDITIONAL_ELIM,
            rule_symbol=self.RULE_SYMBOL_BICONDITIONAL,
            rule_type=self.LogicRules.Types.ELIM  # 명시적으로 Types.ELIM 지정
        )

        # 첫 번째 테이블 (P ↔ Q ⊢ P → Q)
        left_table_data = [
            [PropositionalLogicTable.make_step_number(1),
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.BICONDITIONAL)}Q"],
            [PropositionalLogicTable.EMPTY_CELL,
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.CONDITIONAL)}Q"]
        ]

        # 두 번째 테이블 (P ↔ Q ⊢ Q → P)
        right_table_data = [
            [PropositionalLogicTable.make_step_number(1),
                f"P{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.BICONDITIONAL)}Q"],
            [PropositionalLogicTable.EMPTY_CELL,
                f"Q{PropositionalLogicTable.add_operator_spaces(self.LogicRules.Operators.CONDITIONAL)}P"]
        ]

        # 두 테이블 생성
        left_table = PropositionalLogicTable(
            left_table_data,
            last_premise_index=0
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        right_table = PropositionalLogicTable(
            right_table_data,
            last_premise_index=0
        ).scale(PropositionalLogicTable.TABLE_SCALE)

        # 두 테이블을 그룹으로 묶고 수평 정렬
        tables = VGroup(left_table, right_table).arrange(
            RIGHT, buff=self.TABLE_SPACING)

        self.position_content(title, tables, buff)
        return title, tables

    def construct(self) -> None:
        # 섹션 1: 부정 도입 규칙 (테이블이 큰 경우 - 기본 버퍼 사용)
        self.next_section(self.RULE_NEGATION_INTRO)
        prev_title, prev_table = self.create_negation_intro_section(
            buff=self.BUFF_DEFAULT)
        self.animate_section(prev_title, prev_table)

        # 섹션 2: 부정 제거 규칙 (테이블이 작은 경우 - 큰 버퍼로 중앙 정렬 효과)
        self.next_section(self.RULE_NEGATION_ELIM)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_negation_elim_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)

        # 섹션 3: 논리곱 도입 규칙
        self.next_section(self.RULE_CONJUNCTION_INTRO)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_conjunction_intro_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)

        # 섹션 4: 논리곱 제거 규칙
        self.next_section(self.RULE_CONJUNCTION_ELIM)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_conjunction_elim_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)

        # 섹션 5: 선언 도입 규칙
        self.next_section(self.RULE_DISJUNCTION_INTRO)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_disjunction_intro_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)

        # 섹션 6: 선언 제거 규칙
        self.next_section(self.RULE_DISJUNCTION_ELIM)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_disjunction_elim_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)

        # 섹션 7: 조건문 도입 규칙
        self.next_section(self.RULE_IMPLICATION_INTRO)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_implication_intro_section(
            buff=self.BUFF_MEDIUM)
        self.animate_section(prev_title, prev_table)

        # 섹션 8: 조건문 제거 규칙
        self.next_section(self.RULE_IMPLICATION_ELIM)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_implication_elim_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)

        # 섹션 9: 쌍조건문 도입 규칙
        self.next_section(self.RULE_BICONDITIONAL_INTRO)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_biconditional_intro_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)

        # 섹션 10: 쌍조건문 제거 규칙
        self.next_section(self.RULE_BICONDITIONAL_ELIM)
        self.remove(prev_title, prev_table)
        prev_title, prev_table = self.create_biconditional_elim_section(
            buff=self.BUFF_LARGE)
        self.animate_section(prev_title, prev_table)
