from perceptron import Perceptron
from typing import Dict, Any, Callable


class PerceptronTrainer:
    """단층 퍼셉트론의 학습을 담당하는 클래스"""

    perceptron: Perceptron
    epoch_callbacks: list[Callable[[Dict[str, Any]], None]]

    def __init__(self, perceptron: Perceptron) -> None:
        """학습기 초기화"""
        self.perceptron = perceptron
        self.epoch_callbacks = []

    def add_epoch_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """에포크 완료 시 호출할 콜백 함수 등록"""
        self.epoch_callbacks.append(callback)

    def train(
        self,
        training_data: list[tuple[list[float], int]],
        epochs: int = 10000,
    ) -> None:
        """
        퍼셉트론 학습 수행

        Args:
            training_data: 학습 데이터 세트
            epochs: 최대 학습 반복 횟수
        """
        learning_rate = self.perceptron.learning_rate

        # 특정 가중치와 바이어스로 예측했을 때의 오류를 계산하는 함수
        def calculate_error_for_weights(weights, bias):
            # 현재 가중치와 바이어스를 임시 저장
            orig_weights = self.perceptron.weights.copy()
            orig_bias = self.perceptron.bias
            
            # 주어진 가중치와 바이어스로 설정
            self.perceptron.weights = weights.copy()
            self.perceptron.bias = bias
            
            # 오류 계산
            total_error = 0
            for inputs, target in training_data:
                prediction = self.perceptron.predict(inputs)
                error = target - prediction
                total_error += abs(error)
            
            # 원래 가중치와 바이어스 복원
            self.perceptron.weights = orig_weights
            self.perceptron.bias = orig_bias
            
            return total_error

        for epoch in range(epochs):
            # 현재 에포크 시작 전의 상태 저장
            prev_weights = self.perceptron.weights.copy()
            prev_bias = self.perceptron.bias
            
            # 현재 학습 진행
            total_error = 0
            for inputs, target in training_data:
                prediction = self.perceptron.predict(inputs)
                error = target - prediction
                total_error += abs(error)

                if error != 0:
                    # 가중치 업데이트
                    for i in range(len(self.perceptron.weights)):
                        weight_delta = learning_rate * error * inputs[i]
                        self.perceptron.update_weight(i, weight_delta)

                    # 바이어스 업데이트
                    bias_delta = learning_rate * error
                    self.perceptron.update_bias(bias_delta)

            # 이전 가중치와 바이어스에 맞는 오류값 계산
            prev_error = calculate_error_for_weights(prev_weights, prev_bias)
            
            # 에포크 콜백 호출
            if self.epoch_callbacks:
                epoch_data = {
                    "epoch": epoch,
                    "total_error": prev_error,  # 이전 가중치에 맞는 오류
                    "weights": prev_weights,  # 이전 가중치
                    "bias": prev_bias,  # 이전 바이어스
                }
                
                print(f"Epoch {epoch}: Total Error {prev_error}")
                print(f"Weights: {prev_weights}, Bias: {prev_bias}")
                
                for callback in self.epoch_callbacks:
                    callback(epoch_data)

            # 오차가 0이면 학습 종료
            if total_error == 0:
                print(f"학습 완료! (epoch {epoch})")
                break
