from manim import *
from mperceptron_layer import MPerceptronLayer
from mperceptron import MPerceptron


class MPerceptronLayerTest(Scene):
    def construct(self):
        # 수평 레이어 테스트
        horizontal_layer = MPerceptronLayer(
            n_perceptrons=10,
            layout_direction="horizontal",
            spacing=0.1,
            perceptron_radius=0.3,
        )
        horizontal_layer.to_edge(LEFT).shift(RIGHT)

        # 각 퍼셉트론에 내부 원과 텍스트 표시
        for p in horizontal_layer.perceptrons:
            p.show_inner_circles(r"x", r"y", r"w")

        # 수직 레이어 테스트
        vertical_layer = MPerceptronLayer(
            n_perceptrons=10,
            layout_direction="vertical",
            spacing=0.1,
            perceptron_radius=0.3,
        )
        vertical_layer.to_edge(RIGHT).shift(LEFT)

        # 각 퍼셉트론에 내부 원과 텍스트 표시
        for p in vertical_layer.perceptrons:
            p.show_inner_circles(r"x", r"y", r"w")

        self.add(horizontal_layer, vertical_layer)
        self.wait(3)


class MPerceptronLayerVerticalTest(Scene):
    def construct(self):
        # 중앙 수직 레이어
        vertical_layer = MPerceptronLayer(
            n_perceptrons=10,
            layout_direction="vertical",
            spacing=0.1,
            perceptron_radius=0.3,
        )

        # 좌측 단일 퍼셉트론
        left_perceptron = MPerceptron(
            radius=0.3, outer_text=r"P_L", layout_direction="horizontal"
        )
        left_perceptron.to_edge(LEFT).shift(RIGHT)

        # 우측 단일 퍼셉트론
        right_perceptron = MPerceptron(
            radius=0.3, outer_text=r"P_R", layout_direction="horizontal"
        )
        right_perceptron.to_edge(RIGHT).shift(LEFT)

        # 좌측 퍼셉트론에서 중간 레이어로의 화살표들
        left_arrows = VGroup()
        for p in vertical_layer.perceptrons:
            arrow = Arrow(
                start=left_perceptron.get_output_point(),
                end=p.get_input_point(),
                stroke_width=0.5,  # 선 두께를 더 얇게
                color=YELLOW,
                buff=0,
                max_tip_length_to_length_ratio=0.015,  # 화살촉 크기를 더 작게
            )
            left_arrows.add(arrow)

        # 중간 레이어에서 우측 퍼셉트론으로의 화살표들
        right_arrows = VGroup()
        for p in vertical_layer.perceptrons:
            arrow = Arrow(
                start=p.get_output_point(),
                end=right_perceptron.get_input_point(),
                stroke_width=0.5,  # 선 두께를 더 얇게
                color=YELLOW,
                buff=0,
                max_tip_length_to_length_ratio=0.015,  # 화살촉 크기를 더 작게
            )
            right_arrows.add(arrow)

        self.add(vertical_layer, left_perceptron, right_perceptron)
        self.add(left_arrows, right_arrows)
        self.wait(3)
