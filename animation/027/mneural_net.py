from typing import Optional, Callable, TypeAlias
from manim import *
from mperceptron_layer import MPerceptronLayer

# 타입 별칭 정의
WeightMatrix: TypeAlias = list[list[list[float]]]
BiasMatrix: TypeAlias = list[list[float]]

# 상수 정의
MIN_OPACITY: float = 0.1
DEFAULT_STROKE_WIDTH: float = 0.5
DEFAULT_ARROW_TIP_RATIO: float = 0
DEFAULT_FILL_OPACITY: float = 0.2
DEFAULT_ANIMATION_TIME: float = 0.5


class MNeuralNet(VGroup):
    """신경망을 표현하는 클래스"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.neuron_layers: list[MPerceptronLayer] = []
        self.layer_connections: list[VGroup] = []  # 레이어 간 연결 화살표 저장

    def create_layer(self, n_perceptrons: int, **kwargs) -> MPerceptronLayer:
        """퍼셉트론 레이어 생성"""
        layer = MPerceptronLayer(n_perceptrons=n_perceptrons, **kwargs)
        self.neuron_layers.append(layer)
        self.add(layer)
        return layer

    def create_layer_connection(
        self,
        from_layer_idx: int,
        to_layer_idx: int,
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        stroke_color: ManimColor = YELLOW,
        max_tip_length_to_length_ratio: float = DEFAULT_ARROW_TIP_RATIO,  # 화살촉을 기본적으로는 표시하지 않음.
    ) -> Optional[VGroup]:
        """두 레이어 사이의 연결 화살표들을 생성"""
        if not (
            0 <= from_layer_idx < len(self.neuron_layers)
            and 0 <= to_layer_idx < len(self.neuron_layers)
        ):
            return None

        from_layer = self.neuron_layers[from_layer_idx]
        to_layer = self.neuron_layers[to_layer_idx]

        # 화살표들을 담을 그룹
        arrows = VGroup()

        # 시작층의 각 퍼셉트론에서 타겟층의 모든 퍼셉트론으로 화살표 생성
        for from_perceptron in from_layer.perceptrons:
            for to_perceptron in to_layer.perceptrons:
                arrow = Arrow(
                    start=from_perceptron.get_output_point(),
                    end=to_perceptron.get_input_point(),
                    stroke_width=stroke_width,
                    color=stroke_color,
                    buff=0,
                    max_tip_length_to_length_ratio=max_tip_length_to_length_ratio,
                )
                arrows.add(arrow)

        self.add(arrows)
        self.layer_connections.append(arrows)
        return arrows

    def normalize_values(
        self, values: list[float], min_opacity: float = MIN_OPACITY
    ) -> list[float]:
        """값들을 불투명도 범위(0.1~1.0)로 정규화"""
        if not values:
            return []

        max_val = max(abs(v) for v in values)
        if max_val == 0:
            return [min_opacity] * len(values)

        return [min_opacity + (1 - min_opacity) * (abs(v) / max_val) for v in values]

    def create_arrows_between_layers(
        self,
        from_layer: MPerceptronLayer,
        to_layer: MPerceptronLayer,
        opacities: list[float],
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        stroke_color: ManimColor = YELLOW,
        max_tip_length_to_length_ratio: float = DEFAULT_ARROW_TIP_RATIO,
    ) -> VGroup:
        """두 레이어 사이의 화살표들을 생성하는 헬퍼 메서드"""
        arrows = VGroup()
        arrow_idx = 0

        for prev_perceptron in from_layer.perceptrons:
            for current_perceptron in to_layer.perceptrons:
                opacity = opacities[arrow_idx]
                if opacity > MIN_OPACITY:
                    arrow = Arrow(
                        start=prev_perceptron.get_output_point(),
                        end=current_perceptron.get_input_point(),
                        stroke_width=stroke_width,
                        color=stroke_color,
                        stroke_opacity=opacity,
                        buff=0,
                        max_tip_length_to_length_ratio=max_tip_length_to_length_ratio,
                    )
                    arrows.add(arrow)
                arrow_idx += 1

        return arrows

    def update_input(
        self,
        input_values: list[float],
        weights: WeightMatrix,
        biases: BiasMatrix,
        activation_fn: Callable[[float], float] = lambda x: max(0, x),
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        stroke_color: ManimColor = YELLOW,
        max_tip_length_to_length_ratio: float = DEFAULT_ARROW_TIP_RATIO,
        opacity_animation_time: float = DEFAULT_ANIMATION_TIME,  # 투명도 변경 애니메이션 시간
        connection_animation_time: float = DEFAULT_ANIMATION_TIME,  # 연결선 표시 애니메이션 시간
    ) -> list[tuple[Animation, float]]:  # (애니메이션, 실행시간) 튜플 리스트 반환
        """신경망의 시각적 상태 업데이트 애니메이션 생성"""
        if not self.neuron_layers:
            return []

        animations = []

        # 1. 입력층 업데이트
        input_layer = self.neuron_layers[0]
        input_opacities = self.normalize_values(input_values, MIN_OPACITY)

        # 입력층 애니메이션 생성
        animations.append(
            (
                self._create_layer_opacity_animation(input_layer, input_opacities),
                opacity_animation_time,
            )
        )

        prev_activations = input_values

        # 2. 은닉층과 출력층 업데이트
        for layer_idx in range(1, len(self.neuron_layers)):
            current_layer = self.neuron_layers[layer_idx]
            layer_weights = weights[layer_idx - 1]
            layer_biases = biases[layer_idx - 1]

            # 활성화 값과 연결 가중치 계산
            current_activations, connection_weights = self._calculate_layer_activations(
                prev_activations, layer_weights, layer_biases, activation_fn
            )

            # 화살표 업데이트 애니메이션
            connection_opacities = self.normalize_values(
                connection_weights, MIN_OPACITY
            )
            connection_anims = self._update_layer_connections(
                layer_idx,
                self.neuron_layers[layer_idx - 1],
                current_layer,
                connection_opacities,
                stroke_width,
                stroke_color,
                max_tip_length_to_length_ratio,
            )
            animations.extend(
                (anim, connection_animation_time) for anim in connection_anims
            )

            # 뉴런 불투명도 업데이트 애니메이션
            neuron_opacities = self.normalize_values(current_activations, MIN_OPACITY)
            animations.append(
                (
                    self._create_layer_opacity_animation(
                        current_layer, neuron_opacities
                    ),
                    opacity_animation_time,
                )
            )

            prev_activations = current_activations

        return animations

    def _calculate_layer_activations(
        self,
        prev_activations: list[float],
        layer_weights: list[list[float]],
        layer_biases: list[float],
        activation_fn: Callable[[float], float],
    ) -> tuple[list[float], list[float]]:
        """레이어의 활성화 값과 연결 가중치를 계산"""
        current_activations = []
        connection_weights = []

        for weights, bias in zip(layer_weights, layer_biases):
            weighted_sum = sum(w * a for w, a in zip(weights, prev_activations)) + bias
            current_activations.append(activation_fn(weighted_sum))
            connection_weights.extend(weights)

        return current_activations, connection_weights

    def _create_layer_opacity_animation(
        self, layer: MPerceptronLayer, opacities: list[float]
    ) -> Animation:
        """레이어 뉴런들의 불투명도 변경 애니메이션 생성"""
        return AnimationGroup(
            *[
                perceptron.main_outer_circle.animate.set_fill(opacity=opacity)
                for perceptron, opacity in zip(layer.perceptrons, opacities)
            ]
        )

    def _update_layer_connections(
        self,
        layer_idx: int,
        from_layer: MPerceptronLayer,
        to_layer: MPerceptronLayer,
        connection_opacities: list[float],
        stroke_width: float,
        stroke_color: ManimColor,
        max_tip_length_to_length_ratio: float,
    ) -> list[Animation]:
        """레이어 간 연결 업데이트 애니메이션 생성"""
        animations = []

        # layer_connections 리스트 자동 확장
        while len(self.layer_connections) <= layer_idx - 1:
            self.layer_connections.append(VGroup())
            self.add(self.layer_connections[-1])

        # 이전 화살표 제거
        old_arrows = self.layer_connections[layer_idx - 1]
        if old_arrows and old_arrows in self.submobjects:
            animations.append(FadeOut(old_arrows))
            self.remove(old_arrows)

        # 새 화살표 생성 및 추가
        new_arrows = self.create_arrows_between_layers(
            from_layer,
            to_layer,
            connection_opacities,
            stroke_width,
            stroke_color,
            max_tip_length_to_length_ratio,
        )
        self.layer_connections[layer_idx - 1] = new_arrows
        self.add(new_arrows)
        animations.append(FadeIn(new_arrows))

        return animations

    def reset_network(self) -> list[VGroup]:
        """신경망을 초기 상태로 즉시 리셋하고 제거할 화살표들을 반환"""
        # 모든 뉴런의 불투명도를 기본값으로 리셋
        for layer in self.neuron_layers:
            for perceptron in layer.perceptrons:
                perceptron.main_outer_circle.set_fill(opacity=DEFAULT_FILL_OPACITY)

        # 제거할 화살표들 수집 및 제거
        arrows_to_remove = [
            arrows
            for arrows in self.layer_connections
            if arrows and arrows in self.submobjects
        ]
        for arrows in arrows_to_remove:
            self.remove(arrows)

        self.layer_connections.clear()
        return arrows_to_remove
