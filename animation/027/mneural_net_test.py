from manim import *
from mneural_net import MNeuralNet


class MNeuralNetVerticalTest(Scene):
    def construct(self):
        neural_net = MNeuralNet()

        input_layer = neural_net.create_layer(
            n_perceptrons=2,
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="I",
            spacing=0.2,
        )

        hidden_layer = neural_net.create_layer(
            n_perceptrons=10,
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="H",
            spacing=0.2,
        )

        output_layer = neural_net.create_layer(
            n_perceptrons=1,
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="O",
            spacing=0.2,
        )

        neural_net.arrange_in_grid(cols=3, buff=5)

        self.play(FadeIn(input_layer), run_time=0.5)
        self.play(FadeIn(hidden_layer), run_time=0.5)
        self.play(FadeIn(output_layer), run_time=0.5)

        layer_connection_1 = neural_net.create_layer_connection(
            from_layer_idx=0, to_layer_idx=1
        )
        layer_connection_2 = neural_net.create_layer_connection(
            from_layer_idx=1, to_layer_idx=2
        )

        self.play(FadeIn(layer_connection_1))
        self.play(FadeIn(layer_connection_2))

        self.wait(3)


class MNeuralNetHorizontalTest(Scene):
    def construct(self):
        neural_net = MNeuralNet()

        input_layer = neural_net.create_layer(
            n_perceptrons=2,
            layout_direction="horizontal",  # 수평 배치로 변경
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="I",
            spacing=0.2,
        )

        hidden_layer = neural_net.create_layer(
            n_perceptrons=10,
            layout_direction="horizontal",  # 수평 배치로 변경
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="H",
            spacing=0.2,
        )

        output_layer = neural_net.create_layer(
            n_perceptrons=1,
            layout_direction="horizontal",  # 수평 배치로 변경
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="O",
            spacing=0.2,
        )

        # 수직으로 배열 (rows=3으로 변경)
        neural_net.arrange_in_grid(rows=3, buff=2)

        self.play(FadeIn(input_layer), run_time=0.5)
        self.play(FadeIn(hidden_layer), run_time=0.5)
        self.play(FadeIn(output_layer), run_time=0.5)

        layer_connection_1 = neural_net.create_layer_connection(
            from_layer_idx=0, to_layer_idx=1
        )
        layer_connection_2 = neural_net.create_layer_connection(
            from_layer_idx=1, to_layer_idx=2
        )

        self.play(FadeIn(layer_connection_1))
        self.play(FadeIn(layer_connection_2))

        self.wait(3)


class MNeuralNetUpdateTest(Scene):
    def construct(self):
        neural_net = MNeuralNet()

        # 간단한 2-3-1 신경망 구성
        input_layer = neural_net.create_layer(
            n_perceptrons=2,
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="I",
            spacing=0.2,
        )

        hidden_layer = neural_net.create_layer(
            n_perceptrons=3,
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="H",
            spacing=0.2,
        )

        output_layer = neural_net.create_layer(
            n_perceptrons=1,
            perceptron_radius=0.3,
            perceptron_outer_text_prefix="O",
            spacing=0.2,
        )

        neural_net.arrange_in_grid(cols=3, buff=2)

        self.play(FadeIn(input_layer), run_time=0.5)
        self.play(FadeIn(hidden_layer), run_time=0.5)
        self.play(FadeIn(output_layer), run_time=0.5)

        # 첫 번째 업데이트: 입력 [1, 0]
        input_values = [1.0, 0.0]
        weights = [
            # 입력층->은닉층 가중치
            [
                [0.8, 0.2],  # 첫 번째 은닉 뉴런으로의 가중치
                [0.4, 0.9],  # 두 번째 은닉 뉴런으로의 가중치
                [0.3, 0.5],  # 세 번째 은닉 뉴런으로의 가중치
            ],
            # 은닉층->출력층 가중치
            [[0.3, 0.5, 0.9]],  # 출력 뉴런으로의 가중치
        ]
        biases = [
            [0.1, 0.1, 0.1],  # 은닉층 바이어스
            [0.1],  # 출력층 바이어스
        ]

        test_inputs = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]

        for input_values in test_inputs:
            self.wait(1)

            # 네트워크 초기화 및 화살표 제거
            arrows_to_remove = neural_net.reset_network()
            for arrows in arrows_to_remove:
                self.remove(arrows)  # Scene에서 직접 제거

            # 새로운 입력값으로 업데이트 (애니메이션 시간 지정)
            update_animations = neural_net.update_input(
                input_values,
                weights,
                biases,
                opacity_animation_time=0.5,
                connection_animation_time=0.5,
            )
            for anim, run_time in update_animations:
                self.play(anim, run_time=run_time)

            self.wait(1)
