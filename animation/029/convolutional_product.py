from manim import *

type GridSize = tuple[int, int]
type GridValues = list[list[int | float | str]]
type ColorScheme = dict[str, str | tuple]


class ConvolutionVisualizer(VGroup):
    # 클래스 상수 정의
    RESULT_PLACEHOLDER_TEMPLATE = "O_{{{}{}}}"  # 결과 테이블 플레이스홀더 템플릿
    RESULT_TEXT_SCALE = 0.4  # 결과 테이블 플레이스홀더 텍스트 크기 비율
    RESULT_VALUE_SCALE = 1.5  # 결과 값 텍스트 크기 비율
    WINDOW_STROKE_WIDTH = 3  # 윈도우 테두리 두께
    WINDOW_FILL_OPACITY = 0.15  # 윈도우 채우기 불투명도
    # 계산식 표시 관련 상수 추가
    CALC_FONT_SCALE = 1.2  # 계산식 폰트 크기 비율 감소
    CALC_SHIFT_DOWN = 2.75  # 계산식 하단 이동 거리는 유지

    def __init__(
        self,
        source_size: GridSize = (4, 4),
        kernel_size: GridSize = (3, 3),
        source_values: GridValues | None = None,
        kernel_values: GridValues | None = None,
        text_font_size: float = 36,
        symbol_font_size: float = 120,
        line_thickness: float = 2,
        source_h_buff: float = 0.6,
        source_v_buff: float = 0.8,
        kernel_h_buff: float = 0.6,
        kernel_v_buff: float = 0.6,
        result_h_buff: float = 0.6,
        result_v_buff: float = 0.6,
        kernel_scale_factor: float = 0.75,
        result_scale_factor: float = 0.6,
        arrangement_buff: float = 0.5,
        source_fill_opacity: float = 0.15,
        kernel_fill_opacity: float = 0.15,
        result_fill_opacity: float = 0.025,
        # 애니메이션 관련 파라미터 추가
        anim_window_move_time: float = 0.5,  # 윈도우 이동 시간
        anim_result_fadein_time: float = 0.5,  # 결과 표시 시간
        anim_wait_time: float = 0.1,  # 각 단계 후 대기 시간 (기존 0.2에서 0.1로 감소)
        colors: ColorScheme | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # 설정 저장
        self.source_size = source_size
        self.kernel_size = kernel_size
        self.text_font_size = text_font_size
        self.symbol_font_size = symbol_font_size
        self.line_thickness = line_thickness
        self.source_h_buff = source_h_buff
        self.source_v_buff = source_v_buff
        self.kernel_h_buff = kernel_h_buff
        self.kernel_v_buff = kernel_v_buff
        self.result_h_buff = result_h_buff
        self.result_v_buff = result_v_buff
        self.kernel_scale_factor = kernel_scale_factor
        self.result_scale_factor = result_scale_factor
        self.arrangement_buff = arrangement_buff
        self.source_fill_opacity = source_fill_opacity
        self.kernel_fill_opacity = kernel_fill_opacity
        self.result_fill_opacity = result_fill_opacity

        # 결과 크기 계산
        self.result_size = (
            source_size[0] - kernel_size[0] + 1,
            source_size[1] - kernel_size[1] + 1,
        )

        # 색상 초기화
        self.colors = self._initialize_colors(colors)

        # 기본 데이터 생성
        if source_values is None:
            source_values = self._create_default_source_values()
        if kernel_values is None:
            kernel_values = self._create_default_kernel_values()
        self.source_values = source_values
        self.kernel_values = kernel_values

        # 테이블과 기호 생성
        self._create_source_table()
        self._create_conv_symbol()
        self._create_kernel_table()
        self._create_equals_sign()
        self._create_result_table()

        # 크기 조정 및 배치
        self._adjust_sizes()
        self._arrange_elements()

        # 애니메이션 설정 저장
        self.anim_window_move_time = anim_window_move_time
        self.anim_result_fadein_time = anim_result_fadein_time
        self.anim_wait_time = anim_wait_time

    def _initialize_colors(self, user_colors: ColorScheme | None) -> ColorScheme:
        """색상 스키마를 초기화하고 사용자 정의 색상을 적용"""
        # 뮤지컬 위키드 스타일의 색상 스키마 설정
        default_colors = {
            # 엘파바 스타일 (녹색 계열) - 소스 테이블
            "source_fill": "#1B5E20",
            "source_stroke": "#4CAF50",
            "source_text": "#FFFFFF",
            # 글린다 스타일 (핑크/보라 계열) - 커널 테이블
            "kernel_fill": "#AD1457",
            "kernel_stroke": "#E91E63",
            "kernel_text": "#FFFFFF",
            # 오즈 스타일 (금색/노란색 계열) - 결과 테이블 (밝게 조정)
            "result_fill": "#FB8C00",  # 더 밝은 주황색/금색 (이전: #F57F17)
            "result_stroke": "#FFB74D",  # 더 밝은 강조 색상 (이전: #FFC107)
            "result_text": "#3E2723",  # 약간 더 밝은 갈색 (이전: #212121)
            # 마법 기호 스타일 - 밝은 색상으로 변경
            "symbol_color": "#F8BBD0",
        }

        # 사용자 정의 색상이 있으면 기본값 업데이트
        if user_colors is not None:
            default_colors.update(user_colors)

        return default_colors

    def _create_default_source_values(self) -> GridValues:
        """소스 테이블에 대한 기본 값 생성"""
        values = []
        count = 1
        for i in range(self.source_size[0]):
            row = []
            for j in range(self.source_size[1]):
                row.append(count)
                count += 1
            values.append(row)
        return values

    def _create_default_kernel_values(self) -> GridValues:
        """커널 테이블에 대한 기본 값 생성 (대각선 패턴)"""
        values = []
        for i in range(self.kernel_size[0]):
            row = []
            for j in range(self.kernel_size[1]):
                if i == j or i + j == self.kernel_size[0] - 1:
                    row.append(1)
                else:
                    row.append(0)
            values.append(row)
        return values

    def _create_source_table(self) -> None:
        """소스 테이블 생성"""
        self.source_table = Table(
            self.source_values,
            include_outer_lines=True,
            line_config={
                "stroke_width": self.line_thickness,
                "stroke_color": self.colors["source_stroke"],
            },
            element_to_mobject=lambda value: Text(
                str(value),
                font_size=self.text_font_size,
                color=self.colors["source_text"],
            ),
            h_buff=self.source_h_buff,
            v_buff=self.source_v_buff,
        )

        # 배경색 추가
        self._add_background_to_table(
            self.source_table,
            self.colors["source_fill"],
            opacity=self.source_fill_opacity,
        )

    def _create_conv_symbol(self) -> None:
        """합성곱 기호 생성"""
        self.conv_symbol = MathTex(
            r"\circledast",
            font_size=self.symbol_font_size,
            color=self.colors["symbol_color"],
        )

    def _create_kernel_table(self) -> None:
        """커널 테이블 생성"""
        self.kernel_table = Table(
            self.kernel_values,
            include_outer_lines=True,
            line_config={
                "stroke_width": self.line_thickness,
                "stroke_color": self.colors["kernel_stroke"],
            },
            element_to_mobject=lambda value: Text(
                str(value),
                font_size=self.text_font_size,
                color=self.colors["kernel_text"],
            ),
            h_buff=self.kernel_h_buff,
            v_buff=self.kernel_v_buff,
        )

        # 배경색 추가
        self._add_background_to_table(
            self.kernel_table,
            self.colors["kernel_fill"],
            opacity=self.kernel_fill_opacity,
        )

    def _create_equals_sign(self) -> None:
        """등호 기호 생성"""
        self.equals_sign = MathTex(
            "=", font_size=self.symbol_font_size, color=self.colors["symbol_color"]
        )

    def _create_result_table(self) -> None:
        """결과 테이블 생성"""
        # 위치 정보를 담은 플레이스홀더로 초기화
        result_values = [
            [
                self.RESULT_PLACEHOLDER_TEMPLATE.format(i + 1, j + 1)
                for j in range(self.result_size[1])
            ]
            for i in range(self.result_size[0])
        ]
        self.result_table = Table(
            result_values,
            include_outer_lines=True,
            line_config={
                "stroke_width": self.line_thickness,
                "stroke_color": self.colors["result_stroke"],
            },
            element_to_mobject=lambda value: MathTex(
                value,
                font_size=self.text_font_size * self.RESULT_TEXT_SCALE,
                color=GRAY_D,
            ),
            h_buff=self.result_h_buff,
            v_buff=self.result_v_buff,
        )

        self._add_background_to_table(
            self.result_table,
            self.colors["result_fill"],
            opacity=self.result_fill_opacity,
        )

    def _adjust_sizes(self) -> None:
        """테이블 크기 조정"""
        # 커널 테이블 크기 조정
        kernel_scale = (
            self.source_table.height
            * self.kernel_scale_factor
            / self.kernel_table.height
        )
        self.kernel_table.scale(kernel_scale)

        # 결과 테이블 크기 조정
        result_scale = (
            self.source_table.height
            * self.result_scale_factor
            / self.result_table.height
        )
        self.result_table.scale(result_scale)

    def _arrange_elements(self) -> None:
        """모든 요소 VGroup에 추가하고 수평으로 배치"""
        # VGroup에 모든 요소 추가
        self.add(
            self.source_table,
            self.conv_symbol,
            self.kernel_table,
            self.equals_sign,
            self.result_table,
        )

        # arrange 메소드를 사용하여 요소들을 수평으로 균등하게 배치
        self.arrange(direction=RIGHT, buff=self.arrangement_buff)

    def _add_background_to_table(
        self, table: Table, color: str, opacity: float = 0.8
    ) -> None:
        """테이블의 각 셀에 배경색을 추가하는 헬퍼 메소드"""
        for i in range(len(table.get_rows())):
            for j in range(len(table.get_columns())):
                cell = table.get_cell((i, j))
                background = Rectangle(
                    width=cell.width,
                    height=cell.height,
                    fill_color=color,
                    fill_opacity=opacity,
                    stroke_opacity=0,
                )
                background.move_to(cell.get_center())
                table.add_to_back(background)

    def _create_calculation_formula(self, i: int, j: int, conv_result: int) -> MathTex:
        """현재 윈도우 위치의 계산식 생성"""
        terms = []
        # 모든 항 표시 (0 곱셈 포함)
        for ki in range(self.kernel_size[0]):
            for kj in range(self.kernel_size[1]):
                source_i, source_j = i + ki, j + kj
                kernel_val = self.kernel_values[ki][kj]
                source_val = self.source_values[source_i][source_j]
                # 항 추가 - 괄호 없이 표시
                terms.append(f"{kernel_val} \\cdot {source_val}")

        # 항들을 '+' 로 연결하고 '=' 결과값 추가
        formula = " + ".join(terms) + f" = {conv_result}"

        return MathTex(
            formula,
            font_size=self.text_font_size * self.CALC_FONT_SCALE,
            color=WHITE,
        ).shift(DOWN * self.CALC_SHIFT_DOWN)

    def show_convolution_product_process(self, scene: Scene) -> None:
        """합성곱 연산 과정을 애니메이션으로 시각화"""
        highlight_window = self._create_kernel_sized_window()
        scene.play(Create(highlight_window))

        # 계산식 표시용 변수 (이전 수식 제거를 위해)
        current_formula = None
        convolution_results = []

        for i in range(self.result_size[0]):
            row_results = []
            for j in range(self.result_size[1]):
                # 윈도우 이동
                window_position = self._get_window_position(i, j)
                scene.play(
                    highlight_window.animate.move_to(window_position["center"]),
                    run_time=self.anim_window_move_time,
                )

                # 결과 계산
                conv_result = self._calculate_window_result(i, j)
                row_results.append(conv_result)

                # 이전 계산식 제거
                if current_formula:
                    scene.remove(current_formula)

                # 새 계산식 표시
                current_formula = self._create_calculation_formula(i, j, conv_result)
                scene.play(
                    Write(current_formula),
                    run_time=self.anim_result_fadein_time,
                )

                # 결과 표시
                target_entry = self.result_table.get_entries((i + 1, j + 1))
                result_text = MathTex(
                    str(conv_result),
                    font_size=self.text_font_size * self.RESULT_VALUE_SCALE,
                    color=WHITE,
                ).move_to(target_entry)
                target_entry.become(result_text)

                scene.wait(self.anim_wait_time)

            convolution_results.append(row_results)

        # 마지막 계산식 제거
        if current_formula:
            scene.remove(current_formula)

        self.convolution_results = convolution_results
        return highlight_window

    def _create_kernel_sized_window(self) -> Rectangle:
        """커널 크기와 정확히 일치하는 윈도우 생성"""
        source_cell = self.source_table.get_cell((1, 1))
        window_width = source_cell.width * self.kernel_size[1]
        window_height = source_cell.height * self.kernel_size[0]
        window_position = self._get_window_position(0, 0)

        window = Rectangle(
            width=window_width,
            height=window_height,
            stroke_color=self.colors["kernel_stroke"],
            stroke_width=self.WINDOW_STROKE_WIDTH,
            fill_color=self.colors["kernel_fill"],
            fill_opacity=self.WINDOW_FILL_OPACITY,
        )
        window.move_to(window_position["center"])
        return window

    def _get_window_position(self, top_row: int, left_col: int) -> dict:
        """특정 셀 위치에서의 윈도우 위치 계산 (마님의 1-based 인덱싱 조정)"""
        # 마님은 1-based 인덱싱을 사용하므로, 0-based에서 1-based로 변환
        manim_top_row = top_row + 1
        manim_left_col = left_col + 1
        manim_bottom_right_row = manim_top_row + self.kernel_size[0] - 1
        manim_bottom_right_col = manim_left_col + self.kernel_size[1] - 1

        # 윈도우의 좌상단과 우하단 셀
        top_left_cell = self.source_table.get_cell((manim_top_row, manim_left_col))
        bottom_right_cell = self.source_table.get_cell(
            (manim_bottom_right_row, manim_bottom_right_col)
        )

        # 윈도우 중심 좌표
        center_x = (top_left_cell.get_left()[0] + bottom_right_cell.get_right()[0]) / 2
        center_y = (top_left_cell.get_top()[1] + bottom_right_cell.get_bottom()[1]) / 2
        center = np.array([center_x, center_y, 0])

        # 윈도우 크기
        width = bottom_right_cell.get_right()[0] - top_left_cell.get_left()[0]
        height = top_left_cell.get_top()[1] - bottom_right_cell.get_bottom()[1]

        return {"center": center, "width": width, "height": height}

    def _calculate_window_result(self, top_left_i: int, top_left_j: int) -> int:
        """특정 윈도우 위치에서의 합성곱 결과 계산"""
        result = 0
        for i in range(self.kernel_size[0]):
            for j in range(self.kernel_size[1]):
                source_i, source_j = top_left_i + i, top_left_j + j
                kernel_val = self.kernel_values[i][j]
                source_val = self.source_values[source_i][source_j]
                result += kernel_val * source_val
        return result


class SimpleConvolutionalProduct(Scene):
    def construct(self) -> None:
        self.next_section("Initial Setup")

        # 재사용 가능한 ConvolutionVisualizer 클래스를 사용
        conv_vis = ConvolutionVisualizer(
            source_size=(4, 4),
            kernel_size=(3, 3),
            anim_window_move_time=0.4,  # 윈도우 이동 시간 조정
            anim_result_fadein_time=0.3,  # 결과 표시 시간 조정
            anim_wait_time=2,  # 각 단계 후 대기 시간 조정
        ).shift(UP * 0.8)

        self.play(FadeIn(conv_vis))
        self.wait(1)

        self.next_section("Convolution Operation")

        # 합성곱 연산 애니메이션 진행
        highlight_window = conv_vis.show_convolution_product_process(self)
        self.play(FadeOut(highlight_window))

        # final wait
        self.wait(2)
