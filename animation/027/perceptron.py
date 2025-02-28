from typing import Self, Callable, List, Dict, Any, Optional


class Perceptron:
    """단층 퍼셉트론의 기본 구조와 순방향 추론을 담당하는 클래스"""

    weights: list[float]
    bias: float

    def __init__(self) -> None:
        """퍼셉트론 초기화"""
        self.weights = [0.0, 0.0]
        self.bias = 0.0

    def update_weight(self, index: int, value: float) -> None:
        """가중치 업데이트"""
        self.weights[index] += value

    def update_bias(self, value: float) -> None:
        """바이어스 업데이트"""
        self.bias += value

    @staticmethod
    def step_function(x: float) -> int:
        """계단 함수 (활성화 함수)"""
        return 1 if x > 0 else 0

    def predict(self, inputs: list[float]) -> int:
        """순방향 추론 (forward propagation)"""
        # 입력값과 가중치의 곱의 합에 바이어스를 더함
        summation = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias
        # 활성화 함수 적용하여 출력 계산
        return self.step_function(summation)
