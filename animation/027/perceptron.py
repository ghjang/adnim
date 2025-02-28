from typing import Callable


def step_function(x: float) -> int:
    """계단 함수 (활성화 함수)"""
    return 1 if x > 0 else 0


class Perceptron:
    """단층 퍼셉트론의 기본 구조와 순방향 추론을 담당하는 클래스"""

    input_weights: list[float]
    input_bias: float

    activation_function: Callable[[float], int]

    def __init__(
        self, activation_function: Callable[[float], int] = step_function
    ) -> None:
        """퍼셉트론 초기화"""
        self.input_weights = [0.0, 0.0]
        self.input_bias = 0.0

        self.activation_function = activation_function

    def get_output(self, inputs: list[float]) -> int:
        """퍼셉트론의 출력을 반환"""
        return self.predict(inputs)

    def update_input_weight(self, index: int, value: float) -> None:
        """가중치 업데이트"""
        self.input_weights[index] += value

    def update_input_bias(self, value: float) -> None:
        """바이어스 업데이트"""
        self.input_bias += value

    def predict(self, inputs: list[float]) -> int:
        """순방향 추론 (forward propagation)"""
        summation = (
            sum(w * x for w, x in zip(self.input_weights, inputs)) + self.input_bias
        )
        return self.activation_function(summation)
