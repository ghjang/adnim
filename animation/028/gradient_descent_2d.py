import numpy as np
from manim import *
from typing import Callable, Union, Any


# 비대칭을 강조한 W형태 함수
def f(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    return 0.2 * (1.5 * x**4 - 3.9 * x**2 + 3 * x) + 1.35


def numerical_diff(f: Callable[[float], float], x: float) -> float:
    h: float = 1e-4
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_gradient(f: Callable[[np.ndarray], float], x: np.ndarray) -> np.ndarray:
    grad: np.ndarray = np.zeros_like(x)

    for i in range(x.size):
        tmp_val = x[i]  # 원래 값 저장

        def f_partial(t: float) -> float:
            x[i] = t  # 임시로 값 변경
            ret = f(x)
            x[i] = tmp_val  # 원래 값 복원
            return ret

        grad[i] = numerical_diff(f_partial, tmp_val)

    return grad


# gradient descent 관련 전역 상수
LEARNING_RATE: float = (
    # 0.2  # 시각화 대상 함수에 대해서 정상적으로 최소값을 찾지 못하는 학습률
    0.25  # 시각화 대상 함수에 대해서 정상적으로 최소값을 찾는 학습률
)
# LEARNING_RATE: float = 0.25 # 시각화 대상 함수에 대해서 정상적으로 최소값을 찾는 학습률
MAX_ITER: int = 10


def gradient_descent(
    f: Callable[[np.ndarray], float], init_x: np.ndarray
) -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray], list[float]]:
    x: np.ndarray = init_x
    x_history: list[np.ndarray] = [x.copy()]
    grad_history: list[np.ndarray] = []
    f_history: list[float] = [f(x)]

    for i in range(MAX_ITER):
        grad = numerical_gradient(f, x)
        x -= LEARNING_RATE * grad

        # 히스토리 저장
        x_history.append(x.copy())
        grad_history.append(grad)
        f_history.append(f(x))

    return x, x_history, grad_history, f_history


class GradientDescent2D(ZoomedScene):
    # 줌 관련 상수 수정
    ZOOM_FACTOR: float = 0.3
    ZOOMED_DISPLAY_WIDTH: float = 10
    ZOOMED_DISPLAY_HEIGHT: float = 10
    ZOOM_BUFF: float = 0.2

    def __init__(self):
        ZoomedScene.__init__(
            self,
            zoom_factor=self.ZOOM_FACTOR,
            zoomed_display_width=self.ZOOMED_DISPLAY_WIDTH,
            zoomed_display_height=self.ZOOMED_DISPLAY_HEIGHT,
        )
        super().__init__()

    # 클래스 상수 정의
    PLANE_X_RANGE: tuple[int, int] = (-10, 10)
    PLANE_Y_RANGE: tuple[int, int] = (-8, 12)
    PLOT_X_RANGE: tuple[int, int] = (-3, 3)
    PLANE_SCALE: float = 1.3
    INIT_X: float = 2.0

    # 스타일 상수
    STROKE_OPACITY: float = 0.5
    FONT_SIZE: int = 22
    ARROW_TIP_RATIO: float = 0.2
    ARROW_STROKE_WIDTH: float = 6

    # Z-index 상수 정의 - 한 번만 정의하고 값 차이를 크게
    TANGENT_Z_INDEX: int = 1  # 접선이 가장 아래
    PATH_Z_INDEX: int = 5  # 경로는 중간 레벨
    DOT_Z_INDEX: int = 15  # 점은 더 위에
    ARROW_Z_INDEX: int = 20  # 화살표는 최상위

    # 화살표 관련 상수 추가
    ARROW_MIN_TIP_LENGTH: float = 0.2  # 최소 화살표 끝 크기
    ARROW_MIN_STROKE_WIDTH: float = 6  # 최소 선 두께

    # 애니메이션 타이밍
    STEP_DURATION: float = 0.5
    FADE_DURATION: float = 0.3
    WAIT_DURATION: float = 0.3
    FINAL_WAIT: float = 3.0

    # 레이블 상수 추가
    LABEL_BUFF: float = 0.35  # 레이블 간 간격

    # 접선 관련 상수 수정
    TANGENT_BASE_LENGTH: float = 4.0  # 기본 접선 길이
    TANGENT_MIN_LENGTH: float = 2.0  # 최소 접선 길이
    TANGENT_SCALE: float = 2.0  # gradient 크기에 대한 스케일 팩터
    TANGENT_COLOR = YELLOW_B  # 접선 색상 변경
    TANGENT_STROKE_WIDTH: float = 2.5  # 선 두께 약간 감소
    TANGENT_DASH_LENGTH: float = 0.05  # 점선 간격 약간 증가

    def create_plane(self) -> NumberPlane:
        return NumberPlane(
            x_range=self.PLANE_X_RANGE,
            y_range=self.PLANE_Y_RANGE,
            axis_config={"stroke_opacity": self.STROKE_OPACITY},
            background_line_style={"stroke_opacity": self.STROKE_OPACITY},
        )

    def create_dot(self, pos: np.ndarray, color: str) -> Dot:
        # z-index 명시적으로 설정
        return Dot(pos, color=color, z_index=self.DOT_Z_INDEX)

    def create_arrow(self, start: np.ndarray, end: np.ndarray) -> Arrow:
        """정확한 위치를 가리키는 화살표 생성, 시각적으로 잘 보이게 처리"""
        direction = end - start
        length = np.linalg.norm(direction)

        # 작은 이동에는 화살표 끝과 선 두께만 키움 (위치는 그대로)
        tip_ratio = min(0.5, self.ARROW_TIP_RATIO / max(0.1, length))

        return Arrow(
            start=start,
            end=end,
            color=PURPLE_B,
            buff=0,
            max_tip_length_to_length_ratio=tip_ratio,
            stroke_width=self.ARROW_MIN_STROKE_WIDTH,
        ).set_z_index(self.ARROW_Z_INDEX)

    def create_path_segment(self, start: np.ndarray, end: np.ndarray) -> VMobject:
        path = VMobject(color=GREEN, z_index=self.PATH_Z_INDEX)
        path.set_points_smoothly([start, end])
        return path

    def create_tangent_line(
        self, point: np.ndarray, gradient: float, length: float = None
    ) -> DashedLine:
        """주어진 점에서 기울기를 가진 접선 생성
        gradient의 크기에 따라 접선 길이가 동적으로 조정됨"""
        if length is None:
            # gradient 크기에 따른 길이 계산
            grad_length = np.abs(gradient) * self.TANGENT_SCALE
            length = max(
                self.TANGENT_MIN_LENGTH, min(self.TANGENT_BASE_LENGTH, grad_length)
            )

        # 점에서 양쪽으로 확장된 접선의 시작점과 끝점 계산
        dx = length / np.sqrt(1 + gradient**2)
        dy = gradient * dx

        start = np.array([point[0] - dx, point[1] - dy, 0])
        end = np.array([point[0] + dx, point[1] + dy, 0])

        return DashedLine(
            start=start,
            end=end,
            color=self.TANGENT_COLOR,
            stroke_width=self.TANGENT_STROKE_WIDTH,
            dash_length=self.TANGENT_DASH_LENGTH,
            z_index=self.TANGENT_Z_INDEX,
        )

    def initial_setup(self) -> tuple[NumberPlane, VMobject, MathTex]:
        plane = self.create_plane()
        self.add(plane)

        plot = plane.plot(lambda x: f(x), x_range=self.PLOT_X_RANGE, color=RED)
        self.add(plot)

        # 함수식 LaTeX 생성
        function_formula = MathTex(
            r"f(x) = 0.2 \cdot (1.5 \cdot x^4 - 3.9 \cdot x^2 + 3 \cdot x) + 1.35",
            font_size=40,
            color=YELLOW,
        )
        function_formula.to_edge(DOWN, buff=1)
        self.add(function_formula)

        return plane, plot, function_formula

    def create_labels(self) -> tuple[Text, Text, Text, Text]:
        """4개의 정보 레이블 생성"""
        iter_label = Text("Iteration: 0", font_size=self.FONT_SIZE).to_corner(
            UL, buff=self.LABEL_BUFF
        )

        lr_label = (
            Text(f"Learning Rate: {LEARNING_RATE:.2f}", font_size=self.FONT_SIZE)
            .next_to(iter_label, DOWN, buff=self.LABEL_BUFF)
            .align_to(iter_label, LEFT)
        )

        x_label = (
            Text(f"Current X: {self.INIT_X:.7g}", font_size=self.FONT_SIZE)
            .next_to(lr_label, DOWN, buff=self.LABEL_BUFF)
            .align_to(lr_label, LEFT)
        )

        grad_label = (
            Text("Gradient: 0", font_size=self.FONT_SIZE)
            .next_to(x_label, DOWN, buff=self.LABEL_BUFF)
            .align_to(x_label, LEFT)
        )

        return iter_label, lr_label, x_label, grad_label

    def setup_zoom_display(self, point: np.ndarray) -> None:
        # 줌 카메라 프레임 설정
        self.zoomed_camera.frame.move_to(point)

        # 줌 디스플레이 위치 설정 (우하단)
        self.zoomed_display.to_corner(DR, buff=self.ZOOM_BUFF)

        # 줌 활성화
        self.activate_zooming(animate=True)

    def create_gradient_descent_animation(
        self, plane: NumberPlane, plot: VMobject, function_formula: MathTex
    ) -> None:
        # 플롯과 플레인을 함께 스케일 조정하고 함수식 페이드아웃
        self.play(
            VGroup(plane, plot).animate.scale(self.PLANE_SCALE),
            FadeOut(function_formula),
        )

        # 레이블 초기화
        iter_label, lr_label, x_label, grad_label = self.create_labels()
        self.play(
            FadeIn(iter_label), FadeIn(lr_label), FadeIn(x_label), FadeIn(grad_label)
        )

        # Gradient Descent 실행 - lambda 함수 수정
        init_x = np.array([self.INIT_X])
        _, x_history, grad_history, _ = gradient_descent(
            lambda x: f(x[0]), init_x  # float() 대신 인덱싱 사용
        )

        # 시작점과 현재점 생성 - 명시적 인덱싱 사용
        start_x = x_history[0][0]  # 명시적 인덱싱
        start = plane.c2p(start_x, f(start_x))
        start_point = self.create_dot(start, RED)
        current_point = self.create_dot(start, YELLOW)
        self.play(FadeIn(start_point), FadeIn(current_point))

        # Gradient Descent 스텝 애니메이션
        for i in range(len(grad_history)):
            # 이터레이션 카운터와 값들 업데이트
            current_x = x_history[i][0]
            current_grad = grad_history[i][0]

            new_iter_label = Text(
                f"Iteration: {i + 1}", font_size=self.FONT_SIZE
            ).to_corner(UL, buff=self.LABEL_BUFF)

            new_x_label = (
                Text(f"Current X: {current_x:.7g}", font_size=self.FONT_SIZE)
                .next_to(lr_label, DOWN, buff=self.LABEL_BUFF)
                .align_to(lr_label, LEFT)
            )

            new_grad_label = (
                Text(f"Gradient: {current_grad:.7g}", font_size=self.FONT_SIZE)
                .next_to(new_x_label, DOWN, buff=self.LABEL_BUFF)
                .align_to(new_x_label, LEFT)
            )

            self.play(
                Transform(iter_label, new_iter_label),
                Transform(x_label, new_x_label),
                Transform(grad_label, new_grad_label),
                run_time=self.FADE_DURATION,
            )

            # 현재/다음 위치 계산 - 명시적 인덱싱 사용
            current_x = x_history[i][0]  # float() 제거, 명시적 인덱싱
            current_y = f(current_x)
            next_x = x_history[i + 1][0]  # float() 제거, 명시적 인덱싱
            next_y = f(next_x)

            start = plane.c2p(current_x, current_y)
            end = plane.c2p(next_x, next_y)

            # 현재 점에서의 접선 생성
            current_grad = grad_history[i][0]  # 현재 지점의 기울기
            tangent_line = self.create_tangent_line(point=start, gradient=current_grad)

            # 화살표, 점, 경로 생성
            current_arrow = self.create_arrow(start, end)
            next_point = self.create_dot(end, YELLOW)
            path_segment = self.create_path_segment(start, end)

            if i == 1:  # 2번째 이터레이션부터 줌 표시
                self.setup_zoom_display(end)
            elif i > 1:  # 그 이후로는 줌 프레임만 이동
                # 기울기 방향에 따라 줌 프레임 위치 조정
                # 기울기가 양수면 왼쪽 아래에, 음수면 오른쪽 아래에 정렬
                if current_grad > 0:  # 기울기 양수 (우상향)
                    align_direction = LEFT + DOWN
                    shift_direction = LEFT * 0.05 + DOWN * 0.05
                else:  # 기울기 음수 (우하향)
                    align_direction = RIGHT + DOWN
                    shift_direction = RIGHT * 0.05 + DOWN * 0.05

                self.play(
                    self.zoomed_camera.frame.animate.align_to(
                        next_point, align_direction
                    ).shift(shift_direction),
                    run_time=self.FADE_DURATION,
                )

            # 애니메이션 실행 순서 수정
            # 1. 다음 점과 접선 표시
            self.play(
                FadeIn(next_point),
                Create(tangent_line),
                run_time=self.STEP_DURATION,
            )

            # 2. 이동 방향 화살표 표시
            self.play(
                Create(current_arrow),
                run_time=self.STEP_DURATION,
            )
            self.wait(self.WAIT_DURATION)

            # 3. 이전 요소들 제거하고 경로 표시
            self.play(
                FadeOut(current_point),
                FadeOut(current_arrow),
                FadeOut(tangent_line),
                FadeIn(path_segment),
                run_time=self.STEP_DURATION,
            )

            current_point = next_point

            if i == len(grad_history) - 1:  # 마지막 이터레이션에서
                self.play(  # 줌 디스플레이 제거
                    FadeOut(self.zoomed_display),
                    FadeOut(self.zoomed_camera.frame),
                    run_time=self.FADE_DURATION,
                )

    def construct(self: Any) -> None:
        self.next_section("Initial Set-up")
        plane, plot, function_formula = self.initial_setup()
        self.wait(self.FINAL_WAIT / 2)

        self.next_section("Gradient Descent")
        self.create_gradient_descent_animation(plane, plot, function_formula)

        self.wait(self.FINAL_WAIT)
