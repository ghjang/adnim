from typing import Optional, Literal, Callable
from manim import *
from perceptron import Perceptron, step_function


class MPerceptron(VGroup, Perceptron):
    # 클래스 레벨에서 타입 힌트 추가 (Python 3.12 스타일)
    radius: float
    stroke_width: float
    stroke_color: ManimColor
    fill_color: ManimColor
    fill_opacity: float
    layout_direction: str  # 방향 설정 타입 힌트 추가

    # 내부 구성요소에 대한 타입 힌트
    main_outer_circle: Circle
    outer_text: Optional[MathTex]  # 외부원 텍스트에 대한 타입 힌트 추가
    input_circle: Optional[Circle]
    output_circle: Optional[Circle]
    input_to_output_arrow: Optional[Arrow]
    input_text: Optional[MathTex]
    output_text: Optional[MathTex]
    arrow_text: Optional[MathTex]  # 화살표 텍스트 타입 힌트 추가

    def __init__(
        self,
        radius: float = 1.0,
        stroke_width: float = 2.0,
        stroke_color: ManimColor = TEAL,
        fill_color: ManimColor = PINK,
        fill_opacity: float = 0.2,
        outer_text: Optional[str] = None,  # 외부원 텍스트 인자 추가
        layout_direction: Literal[
            "horizontal", "vertical"
        ] = "horizontal",  # 배치 방향 옵션 추가
        activation_function: Callable[[float], int] = step_function,  # 활성화 함수 추가
        **kwargs
    ):
        # VGroup 초기화
        VGroup.__init__(self, **kwargs)

        # Perceptron 초기화
        Perceptron.__init__(self, activation_function=activation_function)

        # 멤버 변수 초기화
        self.radius = radius
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.layout_direction = layout_direction  # 배치 방향 저장

        # 내부 구성요소 초기화
        self.outer_text = None  # 외부원 텍스트 초기화
        self.input_circle = None
        self.output_circle = None
        self.input_to_output_arrow = None
        self.input_text = None
        self.output_text = None
        self.arrow_text = None  # 화살표 텍스트 초기화

        self.main_outer_circle = Circle(
            radius=radius,
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )

        self.add(self.main_outer_circle)

        # 외부원 텍스트가 있으면 표시
        if outer_text:
            self.show_outer_text(outer_text)

    def show_outer_text(
        self,
        text: Optional[str] = None,
        text_scale_factor: float = 1.6,
        text_max_height_ratio: float = 0.75,
    ) -> None:
        """외부원에 텍스트를 표시하는 메소드"""
        # 기존 텍스트 제거
        if self.outer_text is not None:
            self.remove(self.outer_text)
            self.outer_text = None

        if text is None:
            return

        radius = self.main_outer_circle.width / 2

        # 텍스트 생성
        math_text = MathTex(str(text), color=WHITE).scale(radius * text_scale_factor)

        if math_text.height > radius * text_max_height_ratio:
            scale_factor = (radius * text_max_height_ratio) / math_text.height
            math_text.scale(scale_factor)

        math_text.move_to(self.main_outer_circle.get_center())
        self.outer_text = math_text
        self.add(self.outer_text)

    def hide_outer_text(self) -> None:
        """외부원의 텍스트를 숨기는 메소드"""
        if self.outer_text is not None:
            self.remove(self.outer_text)
            self.outer_text = None

    def create_text_for_component(
        self,
        text: Optional[str],
        component: Mobject,
        scale_factor: float,
        max_height_ratio: float,
        radius: float,
    ) -> Optional[MathTex]:
        """
        구성 요소(원, 화살표 등)에 텍스트를 생성하는 유틸리티 메서드
        """
        if text is None:
            return None

        math_text = MathTex(str(text), color=WHITE).scale(radius * scale_factor)

        if math_text.height > radius * max_height_ratio:
            adjust_scale_factor = (radius * max_height_ratio) / math_text.height
            math_text.scale(adjust_scale_factor)

        math_text.move_to(component.get_center())
        return math_text

    def show_arrow_text(
        self,
        text: str,
        arrow: Arrow,
        inner_radius: float,
        text_scale_factor: float,
        text_max_height_ratio: float,
        buff: float,
        direction: np.ndarray = UP,
    ) -> None:
        """
        화살표 위에 텍스트를 표시하는 메서드
        """
        self.arrow_text = self.create_text_for_component(
            text, arrow, text_scale_factor, text_max_height_ratio, inner_radius
        )

        if self.arrow_text:
            self.arrow_text.next_to(arrow, direction, buff=buff)
            self.add(self.arrow_text)

    def show_inner_circles(
        self,
        input_text: Optional[str] = None,
        output_text: Optional[str] = None,
        arrow_text: Optional[str] = None,  # 화살표 위 텍스트를 위한 인자 추가
        inner_radius_ratio: float = 0.33,
        text_scale_factor: float = 1.5,
        text_max_height_ratio: float = 1.5,
        arrow_tip_ratio: float = 0.125,
        arrow_text_buff: float = 0.1,  # 화살표와 텍스트 사이 간격 조절 버퍼
    ) -> None:
        self.hide_inner_circles()

        # 내부 원 표시할 때 외부 텍스트 숨김
        self.outer_text_value = None  # 클래스 인스턴스 변수로 저장
        if self.outer_text is not None:
            self.outer_text_value = self.outer_text.tex_string
            self.hide_outer_text()

        # 공통 속성 가져오기
        radius = self.main_outer_circle.width / 2
        stroke_width = self.main_outer_circle.get_stroke_width()
        stroke_color = self.main_outer_circle.get_stroke_color()
        fill_color = self.main_outer_circle.get_fill_color()
        fill_opacity = self.main_outer_circle.get_fill_opacity()

        inner_radius = radius * inner_radius_ratio

        # 배치 방향에 따른 위치 오프셋 결정
        if self.layout_direction == "horizontal":
            input_position_offset = LEFT
            output_position_offset = RIGHT
            arrow_text_direction = UP  # 수평 방향일 때 화살표 텍스트는 위쪽
        else:  # vertical
            input_position_offset = UP
            output_position_offset = DOWN
            arrow_text_direction = RIGHT  # 수직 방향일 때 화살표 텍스트는 오른쪽

        # 내부 원 생성 함수
        def create_inner_circle(position_offset: np.ndarray) -> Circle:
            circle = Circle(
                radius=inner_radius,
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
            )
            circle.move_to(
                self.main_outer_circle.get_center()
                + position_offset * (radius - inner_radius)
            )
            return circle

        # 내부 원 생성
        self.input_circle = create_inner_circle(input_position_offset)
        self.output_circle = create_inner_circle(output_position_offset)

        self.add(self.input_circle, self.output_circle)

        # 텍스트 생성 및 추가 - 공통 메서드 사용
        self.input_text = self.create_text_for_component(
            input_text,
            self.input_circle,
            text_scale_factor,
            text_max_height_ratio,
            inner_radius,
        )

        self.output_text = self.create_text_for_component(
            output_text,
            self.output_circle,
            text_scale_factor,
            text_max_height_ratio,
            inner_radius,
        )

        if self.input_text:
            self.add(self.input_text)
        if self.output_text:
            self.add(self.output_text)

        # 화살표 추가 - 방향에 따라 시작점과 끝점 조정
        if self.layout_direction == "horizontal":
            input_circle_edge = self.input_circle.get_center() + RIGHT * inner_radius
            output_circle_edge = self.output_circle.get_center() + LEFT * inner_radius
        else:  # vertical
            input_circle_edge = self.input_circle.get_center() + DOWN * inner_radius
            output_circle_edge = self.output_circle.get_center() + UP * inner_radius

        self.input_to_output_arrow = Arrow(
            start=input_circle_edge,
            end=output_circle_edge,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            buff=0,
            max_tip_length_to_length_ratio=arrow_tip_ratio,
        )
        self.add(self.input_to_output_arrow)

        # 화살표 위 텍스트 추가 - 방향에 따라 위치 조정
        if arrow_text:
            self.show_arrow_text(
                arrow_text,
                self.input_to_output_arrow,
                inner_radius,
                text_scale_factor,
                text_max_height_ratio,
                arrow_text_buff,
                arrow_text_direction,  # 방향에 따라 텍스트 위치 조정
            )

    def hide_inner_circles(self) -> None:
        # 모든 내부 요소를 담을 리스트
        elements_to_remove = [
            attr
            for attr in [
                self.input_circle,
                self.output_circle,
                self.input_to_output_arrow,
                self.input_text,
                self.output_text,
                self.arrow_text,  # 화살표 텍스트 제거 추가
            ]
            if attr is not None
        ]

        # 요소가 있으면 한번에 제거
        if elements_to_remove:
            self.remove(*elements_to_remove)

        # 모든 멤버 변수 초기화
        self.input_circle = None
        self.output_circle = None
        self.input_to_output_arrow = None
        self.input_text = None
        self.output_text = None
        self.arrow_text = None  # 화살표 텍스트 초기화 추가

        # 내부 원이 숨겨질 때 외부 텍스트가 있었다면 다시 표시
        if hasattr(self, "outer_text_value") and self.outer_text_value:
            self.show_outer_text(self.outer_text_value)
            self.outer_text_value = None  # 복원 후 값 초기화

    def get_input_point(self) -> np.ndarray:
        """
        입력 포인트 좌표를 반환
        수평 배치: 입력 원의 왼쪽 극점
        수직 배치: 입력 원의 위쪽 극점
        내부 원이 없는 경우에는 주 외부 원의 적절한 위치 반환
        """
        # 내부 원이 표시되어 있는 경우
        if self.input_circle is not None:
            inner_radius = self.input_circle.width / 2
            center = self.input_circle.get_center()

            if self.layout_direction == "horizontal":
                return center + LEFT * inner_radius  # 왼쪽 극점
            else:  # vertical
                return center + UP * inner_radius  # 위쪽 극점

        # 내부 원이 표시되어 있지 않은 경우 외부 원의 적절한 위치 반환
        radius = self.main_outer_circle.width / 2
        center = self.main_outer_circle.get_center()

        if self.layout_direction == "horizontal":
            return center + LEFT * radius  # 외부 원의 왼쪽 극점
        else:  # vertical
            return center + UP * radius  # 외부 원의 위쪽 극점

    def get_output_point(self) -> np.ndarray:
        """
        출력 포인트 좌표를 반환
        수평 배치: 출력 원의 오른쪽 극점
        수직 배치: 출력 원의 아래쪽 극점
        내부 원이 없는 경우에는 주 외부 원의 적절한 위치 반환
        """
        # 내부 원이 표시되어 있는 경우
        if self.output_circle is not None:
            inner_radius = self.output_circle.width / 2
            center = self.output_circle.get_center()

            if self.layout_direction == "horizontal":
                return center + RIGHT * inner_radius  # 오른쪽 극점
            else:  # vertical
                return center + DOWN * inner_radius  # 아래쪽 극점

        # 내부 원이 표시되어 있지 않은 경우 외부 원의 적절한 위치 반환
        radius = self.main_outer_circle.width / 2
        center = self.main_outer_circle.get_center()

        if self.layout_direction == "horizontal":
            return center + RIGHT * radius  # 외부 원의 오른쪽 극점
        else:  # vertical
            return center + DOWN * radius  # 외부 원의 아래쪽 극점


class MPeceptronTempTest(Scene):
    def construct(self):
        # 수평 배치 퍼셉트론
        horizontal_perceptron = MPerceptron(
            outer_text=r"\text{P}_h", layout_direction="horizontal"
        )
        horizontal_perceptron.shift(UP * 1.5)
        self.add(horizontal_perceptron)

        horizontal_perceptron.show_inner_circles(r"\text{I}", r"\text{O}", r"w_{ij}")

        # 수직 배치 퍼셉트론
        vertical_perceptron = MPerceptron(
            outer_text=r"\text{P}_v", layout_direction="vertical"
        )
        vertical_perceptron.shift(DOWN * 1.5)
        self.add(vertical_perceptron)

        vertical_perceptron.show_inner_circles(r"\text{I}", r"\text{O}", r"w_{ij}")

        # 입력/출력 포인트 테스트
        horizontal_input_dot = Dot(color=RED).move_to(
            horizontal_perceptron.get_input_point()
        )
        horizontal_output_dot = Dot(color=GREEN).move_to(
            horizontal_perceptron.get_output_point()
        )

        vertical_input_dot = Dot(color=RED).move_to(
            vertical_perceptron.get_input_point()
        )
        vertical_output_dot = Dot(color=GREEN).move_to(
            vertical_perceptron.get_output_point()
        )

        self.add(
            horizontal_input_dot,
            horizontal_output_dot,
            vertical_input_dot,
            vertical_output_dot,
        )

        self.wait(3)
