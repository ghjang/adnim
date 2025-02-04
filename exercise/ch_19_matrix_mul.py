from manim import *
import numpy as np

# 레이아웃 관련 상수
MATRIX_BUFF = 0.5
EQUALS_BUFF = 0.3
GROUP_BUFF = 0.5
INITIAL_Y_SHIFT = -1.0    # 초기 행렬 그룹의 수직 위치 조정값

# 시각효과 관련 상수
CORNER_RADIUS = 0.2
RECT_PADDING = 0.2
SYMBOL_SCALE = 1.5        # 수학 기호(×, =)의 크기
COPY_HEIGHT_FACTOR = 1.5  # 복제된 요소들의 수직 이동 높이 계수
MARGIN_SHIFT = 0.5        # 복제 이동 시 추가 여백

# 애니메이션 타이밍 관련 상수
WAIT_TIME = 1
WAIT_TIME_SHORT = WAIT_TIME / 2

# Wicked 뮤지컬 테마 색상 정의 (수정된 버전)
WICKED_GREEN = "#2E8B57"      # 더 깊은 에메랄드 녹색 (Elphaba)
WICKED_PINK = "#FF69B4"       # 더 진한 핫핑크 (Glinda)
WICKED_YELLOW = "#FFD700"     # Yellow Brick Road 색상
WICKED_EMERALD = "#50C878"    # Emerald City 색상

# 색상 매핑 재정의
MATRIX_BRACKET_COLOR = WICKED_YELLOW      # 행렬 괄호 - Yellow Brick Road 색상
MATRIX_ENTRY_COLOR = WICKED_EMERALD       # 행렬 내부 숫자 - 에메랄드
HIGHLIGHT_ROW_COLOR = WICKED_PINK         # 행 하이라이트 - 진한 핑크
HIGHLIGHT_COL_COLOR = WICKED_PINK         # 열 하이라이트 - 동일한 핑크
SYMBOL_COLOR = WICKED_YELLOW              # 수학 기호(×, =) - Yellow Brick Road 색상
FORMULA_COLOR = WICKED_GREEN              # 계산식 - Elphaba 녹색

# 전역 데이터: 곱 대상 행렬과 결과 행렬 계산
MATRIX_A = [[1, 2],
            [3, 4]]
MATRIX_B = [[5, 6],
            [7, 8]]
PRODUCT_MATRIX = np.matmul(MATRIX_A, MATRIX_B).tolist()


def generate_mult_formula(matrix_a, matrix_b, row_idx, col_idx):
    """행렬 곱셈의 한 요소에 대한 LaTeX 수식 문자열을 생성"""
    terms = []
    for i in range(len(matrix_b)):
        terms.append(f"{matrix_a[row_idx][i]} \\times {matrix_b[i][col_idx]}")
    return " + ".join(terms)


class MatrixMultiplicationScene(Scene):
    def create_highlight_rect(self, target_mob, color, with_fill=True):
        """하이라이트용 라운드 사각형 생성 (채움 옵션 추가)"""
        rect = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=target_mob.height + RECT_PADDING,
            width=target_mob.width + RECT_PADDING,
            color=color,
            fill_color=color if with_fill else None,  # 채움색 조건부 설정
            fill_opacity=0.2 if with_fill else 0      # 매우 옅은 채움 불투명도
        )
        rect.move_to(target_mob.get_center())
        return rect

    def create_math_symbol(self, symbol, scale=SYMBOL_SCALE, color=SYMBOL_COLOR):
        """수학 기호 생성"""
        return Tex(symbol, color=color).scale(scale)

    def get_matrix_center_x(self, matrix1, matrix2):
        """두 행렬 사이의 중심 x좌표 계산"""
        a_right = matrix1.get_brackets()[1].get_edge_center(RIGHT)
        b_left = matrix2.get_brackets()[0].get_edge_center(LEFT)
        return (a_right[0] + b_left[0]) / 2

    def animate_matrix_copy(self, row1, col1, row_rect, col_rect):
        # 복제시에는 채움 없이 테두리만 있는 사각형 생성
        highlight_row = VGroup(
            self.create_highlight_rect(
                row1, row_rect.get_color(), with_fill=False),
            row1.copy()
        )
        highlight_col = VGroup(
            self.create_highlight_rect(
                col1, col_rect.get_color(), with_fill=False),
            col1.copy()
        )

        # get_height() 대신 height 속성 사용
        extra = highlight_col.height * COPY_HEIGHT_FACTOR + MARGIN_SHIFT
        row_shift = (highlight_col.get_center()[
                     1] + extra) - highlight_row.get_center()[1]

        self.play(
            highlight_row.animate.shift(UP * row_shift),
            highlight_col.animate.shift(UP * extra)
        )
        return highlight_row, highlight_col

    def setup_matrices(self):
        # 행렬 생성 및 색상 설정
        matrix1 = Matrix(MATRIX_A)
        matrix2 = Matrix(MATRIX_B)
        product = Matrix(PRODUCT_MATRIX)
        for m in (matrix1, matrix2, product):
            m.get_brackets().set_color(MATRIX_BRACKET_COLOR)
            m.get_entries().set_color(MATRIX_ENTRY_COLOR)

        # '=' 텍스트 생성
        equals_tex = MathTex("=").set_color(MATRIX_BRACKET_COLOR)

        # VGroup으로 묶어 가운데 정렬
        group = VGroup(matrix1, matrix2, equals_tex, product)
        group.arrange(RIGHT, buff=GROUP_BUFF)
        group.move_to(ORIGIN)
        # 초기 위치를 아래로 조정
        group.shift(UP * INITIAL_Y_SHIFT)

        return matrix1, matrix2, equals_tex, product

    def animate_highlights(self, matrix1, matrix2, row_idx, col_idx, row_rect, col_rect):
        row = matrix1.get_rows()[row_idx]
        col = matrix2.get_columns()[col_idx]

        # 라운드 사각형 이동
        self.play(
            row_rect.animate.move_to(row.get_center()),
            col_rect.animate.move_to(col.get_center())
        )

        # 복제 및 이동
        highlight_row, highlight_col = self.animate_matrix_copy(
            row, col, row_rect, col_rect)
        self.col_highlight_center_y = highlight_col.get_center()[1]

        # 곱셈 기호 배치
        mult_symbol = self.create_math_symbol("×")
        current_center = (highlight_row.get_center() +
                          highlight_col.get_center()) / 2
        desired_x = self.get_matrix_center_x(matrix1, matrix2)
        mult_symbol.move_to(current_center)
        mult_symbol.shift(np.array([desired_x - current_center[0], 0, 0]))
        self.play(Write(mult_symbol))

        return [mult_symbol, highlight_row, highlight_col]

    def animate_product(self, product, row_idx, col_idx):
        target_cell = product.get_entries(
        )[row_idx * len(MATRIX_B[0]) + col_idx]

        # "=" 기호 생성
        eq_symbol = MathTex("=").set_color(SYMBOL_COLOR).scale(SYMBOL_SCALE)
        eq_symbol.move_to(
            np.array([self.equals_x, self.col_highlight_center_y, 0]))
        self.play(Write(eq_symbol))

        # 계산식 생성
        formula = generate_mult_formula(MATRIX_A, MATRIX_B, row_idx, col_idx)
        detailed_calc = MathTex(formula, color=FORMULA_COLOR)
        left_bracket = product.get_brackets()[0].get_edge_center(LEFT)
        detailed_calc.shift(np.array([
            left_bracket[0] - detailed_calc.get_left()[0],
            self.col_highlight_center_y - detailed_calc.get_center()[1],
            0
        ]))
        self.play(Write(detailed_calc))
        self.wait(WAIT_TIME_SHORT)

        # 결과 셀로 변환
        detailed_calc_copy = detailed_calc.copy()
        self.play(ReplacementTransform(detailed_calc_copy, target_cell))

        # 임시 요소들 반환 (제거하지 않고)
        return target_cell, eq_symbol, detailed_calc

    def construct(self):
        matrix1, matrix2, equals_tex, product = self.setup_matrices()
        self.play(Write(matrix1), Write(matrix2))
        self.play(Write(equals_tex))
        self.play(Write(product.get_brackets()))
        self.wait(WAIT_TIME_SHORT)

        self.equals_x = equals_tex.get_x()

        # 초기 하이라이트 사각형 생성
        row = matrix1.get_rows()[0]
        col = matrix2.get_columns()[0]
        row_rect = self.create_highlight_rect(row, HIGHLIGHT_ROW_COLOR)
        col_rect = self.create_highlight_rect(col, HIGHLIGHT_COL_COLOR)
        row_rect.move_to(row.get_center())
        col_rect.move_to(col.get_center())
        self.play(Create(row_rect), Create(col_rect))

        # 행렬 곱셈 애니메이션 실행
        self.animate_matrix_multiplication(
            matrix1, matrix2, product, row_rect, col_rect)

    def animate_matrix_multiplication(self, matrix1, matrix2, product, row_rect, col_rect):
        """행렬 곱셈 전체 과정 애니메이션"""
        total_iterations = len(MATRIX_A) * len(MATRIX_B[0])
        current_iteration = 0

        for i in range(len(MATRIX_A)):
            for j in range(len(MATRIX_B[0])):
                current_iteration += 1
                temp_elements = self.animate_highlights(
                    matrix1, matrix2, i, j, row_rect, col_rect)
                self.wait(WAIT_TIME_SHORT)

                _, eq_symbol, detailed_calc = self.animate_product(
                    product, i, j)

                if current_iteration == total_iterations:
                    self.play(FadeOut(eq_symbol), FadeOut(detailed_calc),
                              FadeOut(*temp_elements), FadeOut(row_rect), FadeOut(col_rect))
                else:
                    self.play(FadeOut(eq_symbol), FadeOut(
                        detailed_calc), FadeOut(*temp_elements))

                self.wait(WAIT_TIME_SHORT)

        self.wait(WAIT_TIME)
