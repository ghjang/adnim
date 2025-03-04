import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 2D에서 정의된 함수 f(x, y)
def f(x, y):
    r2 = x**2 + y**2
    return r2**2 - 4 * r2 + 2 * x + 3 * y + 2


# 3D 그래프 그리기 위한 x, y 좌표 설정
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)  # 각 좌표에 대한 함수 값 계산

# 3D 그래프 플로팅
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(X, Y, Z, cmap="coolwarm", edgecolor="k")

# 축 설정
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_title(
    "Cup-Shaped Function: f(x, y) = (x^2 + y^2)^2 - 4(x^2 + y^2) + 2x + 3y + 2"
)

plt.show()
