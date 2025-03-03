from typing import Optional, Literal
from manim import *
from mperceptron import MPerceptron


class MPerceptronLayer(VGroup):
    """퍼셉트론 레이어를 표현하는 클래스"""

    def __init__(
        self,
        n_perceptrons: int,
        layout_direction: Literal["horizontal", "vertical"] = "vertical",
        spacing: float = 0.5,  # 퍼셉트론 사이의 간격
        perceptron_radius: float = 1.0,
        perceptron_outer_text_scale_factor: float = 1.6,
        perceptron_outer_text_prefix: str = "P",
        stroke_width: float = 2.0,
        stroke_color: ManimColor = TEAL,
        fill_color: ManimColor = PINK,
        fill_opacity: float = 0.2,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.perceptrons: list[MPerceptron] = []

        # 퍼셉트론 생성 및 배치
        for i in range(n_perceptrons):
            # 퍼셉트론 생성
            perceptron = MPerceptron(
                radius=perceptron_radius,
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                outer_text=f"{perceptron_outer_text_prefix}_{{{i+1}}}",  # 여러 자리 숫자도 아래첨자로 표시되도록 중괄호 처리
                outer_text_scale_factor=perceptron_outer_text_scale_factor,
                layout_direction=(
                    "horizontal" if layout_direction == "vertical" else "vertical"
                ),
            )

            # 위치 계산
            if layout_direction == "horizontal":
                perceptron.shift(RIGHT * i * (2 * perceptron_radius + spacing))
            else:  # vertical
                perceptron.shift(DOWN * i * (2 * perceptron_radius + spacing))

            self.perceptrons.append(perceptron)
            self.add(perceptron)

        # 레이어 전체를 원점 중심으로 정렬
        self.center()

    def get_perceptron(self, index: int) -> Optional[MPerceptron]:
        """지정된 인덱스의 퍼셉트론 반환"""
        if 0 <= index < len(self.perceptrons):
            return self.perceptrons[index]
        return None
