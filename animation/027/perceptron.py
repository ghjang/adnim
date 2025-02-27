from typing import Self, Callable, List, Dict, Any, Optional


class Perceptron:
    """단층 퍼셉트론의 기본 구조와 순방향 추론을 담당하는 클래스"""

    weights: list[float]
    bias: float
    learning_rate: float
    update_callbacks: list[Callable[[Dict[str, Any]], None]]

    def __init__(self, learning_rate: float = 0.1) -> None:
        """퍼셉트론 초기화"""
        self.weights = [0.0, 0.0]  # 가중치 초기화
        self.bias = 0.0  # 바이어스 초기화
        self.learning_rate = learning_rate
        self.update_callbacks = []  # 업데이트 콜백 함수 리스트

    def add_update_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """가중치/바이어스 업데이트 시 호출할 콜백 함수 등록"""
        self.update_callbacks.append(callback)

    def update_weight(self, index: int, value: float) -> None:
        """가중치 업데이트"""
        self.weights[index] += value
        self._notify_callbacks()

    def update_bias(self, value: float) -> None:
        """바이어스 업데이트"""
        self.bias += value
        self._notify_callbacks()

    def _notify_callbacks(self) -> None:
        """등록된 모든 콜백 함수에게 현재 상태 알림"""
        state = {
            "weights": self.weights.copy(),
            "bias": self.bias
        }
        for callback in self.update_callbacks:
            callback(state)

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
