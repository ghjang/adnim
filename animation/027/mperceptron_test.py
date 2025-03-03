from manim import *
from mperceptron import MPerceptron


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
