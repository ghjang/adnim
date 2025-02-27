from perceptron import Perceptron
from perceptron_trainer import PerceptronTrainer


def main() -> None:
    # fmt: off
    # AND 게이트 학습 데이터
    training_data = [
        ([0, 0], 0),
        ([0, 1], 0),
        ([1, 0], 0),
        ([1, 1], 1)
    ]
    # fmt: on

    # 퍼셉트론 생성
    perceptron = Perceptron(learning_rate=0.1)

    # 트레이너 생성 및 학습
    trainer = PerceptronTrainer(perceptron)
    trainer.train(training_data)

    # 결과 테스트
    print("\n결과:")
    for inputs, target in training_data:
        prediction = perceptron.predict(inputs)
        print(f"입력: {inputs}, 출력: {prediction}, 정답: {target}")

    # 학습된 가중치와 바이어스 출력
    print(f"\n학습된 가중치: {perceptron.weights}")
    print(f"학습된 바이어스: {perceptron.bias}")


if __name__ == "__main__":
    main()
