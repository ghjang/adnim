from manim import *
from perceptron import Perceptron
from perceptron_trainer import PerceptronTrainer


class AndGateLearningVisualization(Scene):
    # 학습 관련 상수
    LEARNING_RATE = 0.1

    # 좌표평면 관련 상수
    PLANE_SCALE = 1.9
    X_RANGE = [-4.5, 4.5]
    Y_RANGE = [-4.5, 4.5]
    GRAPH_X_RANGE = [-2.5, 2.5]
    GRAPH_Y_RANGE = [-2.5, 2.5]

    # 시각적 요소 관련 상수
    POINT_RADIUS = 0.1
    LABEL_SCALE = 0.7
    FONT_SIZE = 24
    FILL_OPACITY = 0.15
    LINE_COLOR = YELLOW
    REGION_COLOR = RED
    EQUATION_SCALE = 0.5
    TEXT_Z_INDEX = 10
    
    # 색상 관련 상수
    DOT_COLORS = {0: RED, 1: GREEN}
    TEXT_COLOR = "#FFA07A"  # Light Salmon color
    TEXT_LABEL_COLOR = "#FFA07A"  # Light Salmon
    PARAM_COLORS = {
        "w1": "#FF6B6B",  # 붉은 계열
        "w2": "#4ECDC4",  # 청록 계열
        "b": "#FFD93D",  # 노란 계열
    }
    CORRECT_COLOR = GREEN  # 예측 성공 색상
    WRONG_COLOR = RED  # 예측 실패 색상

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 에포크 데이터를 저장할 리스트 초기화
        self.epoch_history = []
        # 데이터 포인트와 레이블 저장
        self.data_points = []
        self.data_dots = {}
        self.data_labels = {}

    def setup(self):
        self._initial_setup()

    def construct(self):
        self.next_section("Initial Setup")

        # 'x1, x2' 데이터 표시를 위한 플레인 생성
        number_plane = self._create_number_plane()
        self.add(number_plane)

        # AND 게이트 입력값 4개에 대한 포인트 생성 및 표시
        self._create_and_display_data_points()

        # 트레이닝 히스토리 표시 섹션
        self.next_section("Show Training History")

        # 트레이닝 히스토리 데이터를 사용하여 결정 경계선 표시
        self._display_training_history(number_plane)

        # final wait
        self.wait(3)

    def _create_number_plane(self) -> NumberPlane:
        """좌표 평면을 생성합니다."""
        return NumberPlane(
            axis_config={"stroke_opacity": 0.5},
            background_line_style={"stroke_opacity": 0.5},
        ).scale(self.PLANE_SCALE)

    def _create_and_display_data_points(self) -> None:
        """AND 게이트 입력값 4개에 대한 포인트와 레이블을 생성하고 표시합니다."""
        self.data_points = [
            {"coords": [0, 0], "output": 0, "label_direction": DOWN},
            {"coords": [0, 1], "output": 0, "label_direction": UP},
            {"coords": [1, 0], "output": 0, "label_direction": DOWN},
            {"coords": [1, 1], "output": 1, "label_direction": UP},
        ]

        for point in self.data_points:
            x, y = point["coords"]
            output = point["output"]
            direction = point["label_direction"]

            # 좌표평면 상의 위치로 변환
            position = self.get_plane_coords(x, y)

            # 점 생성 (초기에는 보이지 않게 - 불투명도 0)
            dot = Dot(
                position,
                color=self.WRONG_COLOR,
                radius=self.POINT_RADIUS,
                fill_opacity=0,
            )
            self.data_dots[(x, y)] = dot
            self.add(dot)

            # 레이블 추가 (초기에는 보이지 않게 - 불투명도 0)
            label = (
                MathTex(f"({x},{y})")
                .next_to(dot, direction, buff=0.1)
                .scale(self.LABEL_SCALE)
                .set_opacity(0)
            )
            self.data_labels[(x, y)] = label
            self.add(label)

    def get_plane_coords(self, x: float, y: float) -> np.ndarray:
        """X, Y 좌표값을 화면 좌표로 변환합니다."""
        # 임시적으로 화면 중앙에서 스케일을 적용하여 좌표 계산
        return np.array([x * self.PLANE_SCALE, y * self.PLANE_SCALE, 0])

    def _format_float(self, value: float) -> str:
        """소수점 이하 불필요한 0을 제거한 문자열 반환"""
        return f"{value:.2f}".rstrip("0").rstrip(".")

    def _create_epoch_text(self, epoch_data: dict) -> VGroup:
        """에포크 데이터를 표시하는 텍스트 그룹을 생성합니다."""
        # 에포크 0인지 확인
        is_epoch_zero = epoch_data["epoch"] == 0

        # 모든 텍스트 요소를 하나의 리스트로 생성
        text_elements = [
            # 기본 정보 (항상 표시)
            MathTex(
                f"\\textrm{{Epoch: }}{epoch_data['epoch']}",
                font_size=self.FONT_SIZE,
                color=self.TEXT_LABEL_COLOR,
            ),
            MathTex(
                f"\\textrm{{Learning Rate: }}{epoch_data['learning_rate']}",
                font_size=self.FONT_SIZE,
                color=self.TEXT_LABEL_COLOR,
            ),
            MathTex(
                f"\\textrm{{Weights: }}[{self._format_float(epoch_data['weights'][0])}, {self._format_float(epoch_data['weights'][1])}]",
                font_size=self.FONT_SIZE,
                color=self.TEXT_LABEL_COLOR,
            ),
            MathTex(
                f"\\textrm{{Bias: }}{self._format_float(epoch_data['bias'])}",
                font_size=self.FONT_SIZE,
                color=self.TEXT_LABEL_COLOR,
            ),
        ]

        # 추가 정보 (에포크 0에서는 숨김)
        additional_texts = [
            # Total Error 텍스트
            MathTex(
                f"\\textrm{{Total Error: }}{self._format_float(epoch_data['total_error'])}",
                font_size=self.FONT_SIZE,
                color=self.TEXT_LABEL_COLOR,
            ),
            # 가중치와 바이어스 업데이트 일반식
            MathTex(
                "\\Delta w_i = \\eta \\cdot e \\cdot x_i,\\,\\,\\,\\Delta b = \\eta \\cdot e",
                font_size=self.FONT_SIZE,
                color=self.TEXT_LABEL_COLOR,
            ),
            # 일반화된 함수식
            MathTex(
                "y = \\left\\{\\frac{-(w_1)}{w_2}\\right\\}\\cdot x + \\left\\{\\frac{-(b)}{w_2}\\right\\}",
                font_size=self.FONT_SIZE,
                color=self.TEXT_LABEL_COLOR,
            ),
        ]

        # 에포크 0에서는 추가 정보 텍스트를 숨기고, 그 외에는 모두 표시
        if is_epoch_zero:
            # 에포크 0에서는 기본 정보만 표시
            all_texts = text_elements
        else:
            # 나머지 에포크에서는 모든 정보 표시
            all_texts = text_elements + additional_texts

        # 모든 텍스트를 그룹으로 결합하고 좌측 정렬로 배치
        text_group = VGroup(*all_texts).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        text_group.set_z_index(self.TEXT_Z_INDEX)

        return text_group

    def _create_equation_text(
        self, weights: list, bias: float, number_plane: NumberPlane
    ) -> MathTex:
        """가중치와 바이어스로부터 함수식 레이텍을 생성합니다."""
        w1, w2 = weights
        b = bias

        if abs(w2) < 1e-10:  # 수직선의 경우
            if abs(w1) < 1e-10:
                return None

            # x = -b/w1 형태
            equation = MathTex(
                "x = \\left\\{\\frac{-("
                + self._format_float(b)
                + ")}{"
                + self._format_float(w1)
                + "}\\right\\}",
                color=self.TEXT_LABEL_COLOR,
            )

            # x_val 계산
            x_val = -b / w1
            equation_x = self._get_safe_x_position(x_val + 0.5)
        else:
            # y = (-w1/w2)x + (-b/w2) 형태
            equation = MathTex(
                "y = "
                "\\left\\{\\frac{-("
                + self._format_float(w1)
                + ")}{"
                + self._format_float(w2)
                + "}\\right\\}"
                "\\cdot x"
                "+\\left\\{\\frac{-("
                + self._format_float(b)
                + ")}{"
                + self._format_float(w2)
                + "}\\right\\}",
                color=self.TEXT_LABEL_COLOR,
            )

            # 위치 계산
            equation_x = self._calculate_equation_position(w1, w2, b)

        equation.scale(self.EQUATION_SCALE)
        equation.next_to(number_plane.c2p(equation_x, -1), RIGHT, buff=0.5)
        equation.set_z_index(self.TEXT_Z_INDEX)

        return equation
        
    def _get_safe_x_position(self, x_val):
        """좌표평면 범위 내의 안전한 X 좌표값을 반환합니다."""
        return max(min(x_val, self.X_RANGE[1] - 1), self.X_RANGE[0] + 1)
        
    def _calculate_equation_position(self, w1, w2, b):
        """함수식 위치를 계산합니다."""
        slope = -w1 / w2
        y_intercept = -b / w2
        
        if abs(slope) < 1e-6:
            return 0
            
        target_y = -1
        x_at_target_y = (target_y - y_intercept) / slope
        return self._get_safe_x_position(x_at_target_y)

    def _draw_decision_boundary_with_region(
        self, number_plane: NumberPlane, weights: list, bias: float
    ) -> tuple[VMobject, VMobject, VMobject]:
        """결정 경계선과 아래쪽 영역, 함수식을 그립니다."""
        w1, w2 = weights
        b = bias

        print(f"Drawing decision boundary: w1={w1}, w2={w2}, b={b}")

        # 모든 가중치와 바이어스가 0인 경우 - y = 0 수평선
        if abs(w1) < 1e-10 and abs(w2) < 1e-10 and abs(b) < 1e-10:
            # y = 0 형태의 수평선
            line = number_plane.plot_line_graph(
                x_values=self.X_RANGE,
                y_values=[0, 0],  # y = 0
                line_color=YELLOW,
                add_vertex_dots=False,
            )

            # 수평선 아래 영역을 채움
            points = [
                number_plane.c2p(self.X_RANGE[0], 0),  # 왼쪽 경계선 점
                number_plane.c2p(self.X_RANGE[1], 0),  # 오른쪽 경계선 점
                number_plane.c2p(
                    self.X_RANGE[1], self.Y_RANGE[0]
                ),  # 오른쪽 아래 모서리
                number_plane.c2p(self.X_RANGE[0], self.Y_RANGE[0]),  # 왼쪽 아래 모서리
            ]

            region = Polygon(
                *points,
                fill_color=self.REGION_COLOR,
                fill_opacity=self.FILL_OPACITY,
                stroke_width=0,
            )

            # 함수식은 y = 0
            equation = MathTex("y = 0", color=self.TEXT_LABEL_COLOR)
            equation.scale(self.EQUATION_SCALE)
            equation.next_to(number_plane.c2p(0, -1), RIGHT, buff=0.5)
            equation.set_z_index(self.TEXT_Z_INDEX)

            # z-index 설정
            region.set_z_index(-1)
            line.set_z_index(0)

            return line, region, equation

        # 특수 케이스 처리: 수직선 (w2 = 0, w1 ≠ 0)
        if abs(w2) < 1e-10:
            # x = -b/w1 형태의 수직선
            x_val = -b / w1
            line = number_plane.plot_line_graph(
                x_values=[x_val, x_val],
                y_values=self.Y_RANGE,
                line_color=YELLOW,
                add_vertex_dots=False,
            )

            # 수직선의 왼쪽 또는 오른쪽 영역을 채움
            points = [
                number_plane.c2p(x_val, self.Y_RANGE[0]),  # 선의 아래 점
                number_plane.c2p(x_val, self.Y_RANGE[1]),  # 선의 위 점
                number_plane.c2p(self.X_RANGE[0], self.Y_RANGE[1]),  # 왼쪽 위 모서리
                number_plane.c2p(self.X_RANGE[0], self.Y_RANGE[0]),  # 왼쪽 아래 모서리
            ]

        else:
            # 일반적인 경우: y = (-w1*x - b) / w2
            slope = -w1 / w2
            y_intercept = -b / w2

            # 직선 그리기
            line = number_plane.plot_line_graph(
                x_values=self.X_RANGE,
                y_values=[
                    self.X_RANGE[0] * slope + y_intercept,
                    self.X_RANGE[1] * slope + y_intercept,
                ],
                line_color=YELLOW,
                add_vertex_dots=False,
            )

            # 아래쪽 영역을 채우기 위한 점들
            points = [
                number_plane.c2p(
                    self.X_RANGE[0], self.X_RANGE[0] * slope + y_intercept
                ),  # 왼쪽 경계선 점
                number_plane.c2p(
                    self.X_RANGE[1], self.X_RANGE[1] * slope + y_intercept
                ),  # 오른쪽 경계선 점
                number_plane.c2p(
                    self.X_RANGE[1], self.Y_RANGE[0]
                ),  # 오른쪽 아래 모서리
                number_plane.c2p(self.X_RANGE[0], self.Y_RANGE[0]),  # 왼쪽 아래 모서리
            ]

        # 영역 생성
        region = Polygon(
            *points,
            fill_color=self.REGION_COLOR,
            fill_opacity=self.FILL_OPACITY,
            stroke_width=0,
        )

        # 함수식 생성
        equation = self._create_equation_text(weights, bias, number_plane)

        # z-index 설정
        region.set_z_index(-1)
        line.set_z_index(0)
        if equation:
            equation.set_z_index(1)

        return line, region, equation

    def _predict_with_weights(self, weights, bias, inputs):
        """주어진 가중치와 바이어스로 예측 결과를 반환합니다."""
        temp_perceptron = Perceptron()
        temp_perceptron.weights = weights.copy()
        temp_perceptron.bias = bias
        return temp_perceptron.predict(inputs)

    def _update_data_point_colors(self, weights, bias):
        """현재 가중치와 바이어스로 예측 결과에 따라 데이터 포인트 색상을 업데이트합니다."""
        animations = []

        for point in self.data_points:
            x, y = point["coords"]
            target = point["output"]
            prediction = self._predict_with_weights(weights, bias, [x, y])

            # 예측 성공/실패에 따른 색상 결정
            new_color = self.CORRECT_COLOR if prediction == target else self.WRONG_COLOR

            # 색상 변경 애니메이션 생성
            dot = self.data_dots[(x, y)]
            animations.append(dot.animate.set_color(new_color))

        return animations

    def _show_data_points(self):
        """데이터 포인트와 레이블을 불투명도 1.0으로 설정하여 보이게 합니다."""
        animations = []

        for coords, dot in self.data_dots.items():
            animations.append(dot.animate.set_fill(opacity=1))

        for coords, label in self.data_labels.items():
            animations.append(label.animate.set_opacity(1))

        return animations

    def _display_training_history(self, number_plane: NumberPlane) -> None:
        """트레이닝 히스토리 데이터를 사용하여 결정 경계선 변화를 애니메이션으로 표시합니다."""
        history_len = len(self.epoch_history)
        if history_len <= 0:
            return

        # 초기 요소들 생성 (에포크 0)
        first_data = self.epoch_history[0]

        # 직선과 영역은 생성하되 화면에 표시하지 않음
        current_line, current_region, current_equation = (
            self._draw_decision_boundary_with_region(
                number_plane, first_data["weights"], first_data["bias"]
            )
        )
        current_text = self._create_epoch_text(first_data)

        # 에포크 0에서는 텍스트만 표시 (직선과 영역은 표시하지 않음)
        self.play(FadeIn(current_text))
        self.wait()

        # 에포크 1부터는 시각적 요소 모두 표시
        if history_len > 1:
            epoch_data = self.epoch_history[1]
            new_line, new_region, new_equation = (
                self._draw_decision_boundary_with_region(
                    number_plane, epoch_data["weights"], epoch_data["bias"]
                )
            )
            new_text = self._create_epoch_text(epoch_data)

            # 데이터 포인트와 레이블을 보이게 만듦 (직접 설정)
            for coords, dot in self.data_dots.items():
                dot.set_fill(opacity=1)  # 직접 불투명도 설정

            for coords, label in self.data_labels.items():
                label.set_opacity(1)  # 직접 불투명도 설정

            # 데이터 포인트 색상 업데이트
            for point in self.data_points:
                x, y = point["coords"]
                target = point["output"]
                # 임시 퍼셉트론으로 예측
                temp_perceptron = Perceptron()
                temp_perceptron.weights = epoch_data["weights"].copy()
                temp_perceptron.bias = epoch_data["bias"]
                prediction = temp_perceptron.predict([x, y])
                # 색상 설정
                new_color = (
                    self.CORRECT_COLOR if prediction == target else self.WRONG_COLOR
                )
                self.data_dots[(x, y)].set_color(new_color)  # 직접 색상 설정

            # 에포크 1의 모든 요소 표시
            animations = [
                FadeIn(new_region),
                FadeIn(new_line),
                ReplacementTransform(current_text, new_text),
            ]

            if new_equation:
                animations.append(FadeIn(new_equation))

            # 모든 데이터 포인트와 레이블을 애니메이션으로 표시
            animations.append(
                AnimationGroup(
                    *[FadeIn(dot) for dot in self.data_dots.values()]
                    + [FadeIn(label) for label in self.data_labels.values()]
                )
            )

            self.play(*animations)
            self.wait()

            # 현재 객체들 업데이트
            current_line = new_line
            current_region = new_region
            current_equation = new_equation
            current_text = new_text

        # 두 번째 에포크부터는 ReplacementTransform 사용
        for i in range(2, history_len):
            epoch_data = self.epoch_history[i]
            new_line, new_region, new_equation = (
                self._draw_decision_boundary_with_region(
                    number_plane, epoch_data["weights"], epoch_data["bias"]
                )
            )
            new_text = self._create_epoch_text(epoch_data)

            # 데이터 포인트 색상 업데이트 애니메이션
            color_animations = self._update_data_point_colors(
                epoch_data["weights"], epoch_data["bias"]
            )

            if new_line and current_line:
                animations = [
                    ReplacementTransform(current_region, new_region),
                    ReplacementTransform(current_line, new_line),
                    ReplacementTransform(current_text, new_text),
                ]
                animations.extend(color_animations)  # 색상 업데이트

                if current_equation and new_equation:
                    animations.append(
                        ReplacementTransform(current_equation, new_equation)
                    )
                elif new_equation:
                    animations.append(FadeIn(new_equation))

                self.play(*animations)
                self.wait()

                # 현재 객체들 업데이트
                current_line = new_line
                current_region = new_region
                current_equation = new_equation
                current_text = new_text

    def _initial_setup(self):
        """초기 설정 및 데이터 학습 수행"""
        # fmt: off
        # AND 게이트 학습 데이터
        training_data = [
            ([0, 0], 0),
            ([0, 1], 0),
            ([1, 0], 0),
            ([1, 1], 1)
        ]
        # fmt: on

        # 퍼셉트론 생성
        perceptron = Perceptron()

        # 트레이너 생성 및 학습
        trainer = PerceptronTrainer(perceptron, learning_rate=self.LEARNING_RATE)
        trainer.add_epoch_callback(self._update_training_data)

        # 애니메이션과 함께 학습 진행
        self.wait(0.5)

        # 시각화를 위한 학습 진행
        trainer.train(training_data)

        # 학습 히스토리 결과 출력
        print(f"\n학습 기록 수집 완료: {len(self.epoch_history)}개의 에포크 데이터")

        # 결과 테스트 및 출력
        self._print_test_results(perceptron, training_data)

    def _print_test_results(self, perceptron: Perceptron, training_data: list) -> None:
        """학습 결과를 테스트하고 콘솔에 출력합니다."""
        print("\n결과:")
        for inputs, target in training_data:
            prediction = perceptron.predict(inputs)
            print(f"입력: {inputs}, 출력: {prediction}, 정답: {target}")

        # 학습된 가중치와 바이어스 출력
        print(f"\n학습된 가중치: {perceptron.weights}")
        print(f"학습된 바이어스: {perceptron.bias}")

    def _update_training_data(self, epoch_data: dict) -> None:
        """에포크 데이터를 기록하고 콘솔에 출력합니다."""
        # 학습률 정보 추가
        self.epoch_history.append(epoch_data)

        epoch = epoch_data["epoch"]
        total_error = epoch_data["total_error"]
        weights = epoch_data["weights"]
        bias = epoch_data["bias"]

        print(f"Epoch {epoch}: Total Error {total_error}")
        print(f"Weights: {weights}, Bias: {bias}")
