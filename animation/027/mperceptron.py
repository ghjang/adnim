from manim import *
from typing import Optional


class MPerceptron(VGroup):
    # 클래스 레벨에서 타입 힌트 추가 (Python 3.12 스타일)
    radius: float
    stroke_width: float
    stroke_color: ManimColor
    fill_color: ManimColor
    fill_opacity: float

    # 내부 구성요소에 대한 타입 힌트
    main_outer_circle: Circle
    outer_text: Optional[MathTex]  # 외부원 텍스트에 대한 타입 힌트 추가
    input_circle: Optional[Circle]
    output_circle: Optional[Circle]
    input_to_output_arrow: Optional[Arrow]
    input_text: Optional[MathTex]
    output_text: Optional[MathTex]

    def __init__(
        self,
        radius: float = 1.0,
        stroke_width: float = 2.0,
        stroke_color: ManimColor = TEAL,
        fill_color: ManimColor = PINK,
        fill_opacity: float = 0.2,
        outer_text: Optional[str] = None,  # 외부원 텍스트 인자 추가
        **kwargs
    ):
        super().__init__(**kwargs)

        # 멤버 변수 초기화
        self.radius = radius
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity

        # 내부 구성요소 초기화
        self.outer_text = None  # 외부원 텍스트 초기화
        self.input_circle = None
        self.output_circle = None
        self.input_to_output_arrow = None
        self.input_text = None
        self.output_text = None

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

        radius = self.main_outer_circle.get_width() / 2

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

    def show_inner_circles(
        self,
        input_text: Optional[str] = None,
        output_text: Optional[str] = None,
        inner_radius_ratio: float = 0.33,
        text_scale_factor: float = 1.5,
        text_max_height_ratio: float = 1.5,
        arrow_tip_ratio: float = 0.125,
    ) -> None:
        self.hide_inner_circles()

        # 내부 원 표시할 때 외부 텍스트 숨김
        self.outer_text_value = None  # 클래스 인스턴스 변수로 저장
        if self.outer_text is not None:
            self.outer_text_value = self.outer_text.tex_string
            self.hide_outer_text()

        # 공통 속성 가져오기
        radius = self.main_outer_circle.get_width() / 2
        stroke_width = self.main_outer_circle.get_stroke_width()
        stroke_color = self.main_outer_circle.get_stroke_color()
        fill_color = self.main_outer_circle.get_fill_color()
        fill_opacity = self.main_outer_circle.get_fill_opacity()

        inner_radius = radius * inner_radius_ratio

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
        self.input_circle = create_inner_circle(LEFT)
        self.output_circle = create_inner_circle(RIGHT)

        self.add(self.input_circle, self.output_circle)

        # 텍스트 생성 함수
        def create_text(text: Optional[str], circle: Circle) -> Optional[MathTex]:
            if text is None:
                return None

            math_text = MathTex(str(text), color=WHITE).scale(
                inner_radius * text_scale_factor
            )

            if math_text.height > inner_radius * text_max_height_ratio:
                scale_factor = (inner_radius * text_max_height_ratio) / math_text.height
                math_text.scale(scale_factor)

            math_text.move_to(circle.get_center())
            return math_text

        # 텍스트 생성 및 추가
        self.input_text = create_text(input_text, self.input_circle)
        self.output_text = create_text(output_text, self.output_circle)

        if self.input_text:
            self.add(self.input_text)
        if self.output_text:
            self.add(self.output_text)

        # 화살표 추가
        input_circle_right = self.input_circle.get_center() + RIGHT * inner_radius
        output_circle_left = self.output_circle.get_center() + LEFT * inner_radius

        self.input_to_output_arrow = Arrow(
            start=input_circle_right,
            end=output_circle_left,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            buff=0,
            max_tip_length_to_length_ratio=arrow_tip_ratio,
        )
        self.add(self.input_to_output_arrow)

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

        # 내부 원이 숨겨질 때 외부 텍스트가 있었다면 다시 표시
        if hasattr(self, "outer_text_value") and self.outer_text_value:
            self.show_outer_text(self.outer_text_value)
            self.outer_text_value = None  # 복원 후 값 초기화


class MPeceptronTempTest(Scene):
    def construct(self):
        perceptron = MPerceptron(outer_text=r"\text{P}")
        self.add(perceptron)

        perceptron.show_inner_circles(r"\text{I}", r"\text{O}")
        self.wait(2)

        perceptron.hide_inner_circles()
        self.wait(2)
