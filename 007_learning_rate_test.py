import numpy as np
from math import sqrt


def gradient_descent_step(x, learning_rate):
    """단일 경사하강법 스텝 계산"""
    gradient = 4 * x * (x**2 - 2)
    return x - learning_rate * gradient


def test_learning_rate(learning_rate, max_steps=100, tolerance=0.001):
    """주어진 학습률로 √2에 수렴하는지 테스트"""
    x = 2.0  # 시작값
    target = sqrt(2)
    steps = []

    for i in range(max_steps):
        steps.append(x)
        if abs(x - target) < tolerance:
            return True, i + 1, steps
        x = gradient_descent_step(x, learning_rate)

        # 발산하는 경우 조기 종료
        if abs(x) > 10 or np.isnan(x):
            return False, i + 1, steps

    return False, max_steps, steps


def main():
    # 테스트할 학습률 범위
    learning_rates = [0.05, 0.08, 0.1, 0.12, 0.15, 0.2]
    target = sqrt(2)

    print(f"목표값: √2 ≈ {target:.6f}")
    print("\n학습률 테스트 결과:")
    print("-" * 60)
    print(f"{'학습률':^10} {'수렴여부':^10} {'스텝수':^10} {'최종값':^15} {'오차':^15}")
    print("-" * 60)

    for lr in learning_rates:
        converged, steps, values = test_learning_rate(lr)
        final_value = values[-1]
        error = abs(final_value - target)

        status = "수렴" if converged else "발산"
        print(
            f"{lr:^10.3f} {status:^10} {steps:^10d} {final_value:^15.6f} {error:^15.6f}")


if __name__ == "__main__":
    main()
