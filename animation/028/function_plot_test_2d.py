import numpy as np
import matplotlib.pyplot as plt


# 비대칭을 더욱 강조한 W형태 함수
def f(x):
    return x**4 - 4 * x**2 + 3 * x  # 마지막 항 계수를 키워 비대칭 강화


# x 범위 설정
x = np.linspace(-3, 3, 400)

# 그래프 그리기
plt.figure(figsize=(8, 5))
plt.plot(x, f(x), label="x^4 - 4x^2 + 3x", color="purple")

plt.axhline(0, color="black", linewidth=0.5)
plt.axvline(0, color="black", linewidth=0.5)
plt.legend()
plt.grid()
plt.show()
