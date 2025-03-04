from manim import *


class LogFunctionPlot(Scene):
    def construct(self):
        # 넘버플레인 생성
        plane = NumberPlane(
            x_range=[0, 10, 1],  # x축 범위를 0부터 시작
            y_range=[0, 5, 1],  # y축 범위 조정
            x_length=6,  # 화면 크기 조정
            y_length=4,
            axis_config={
                "color": BLUE,
                "numbers_to_include": np.arange(0, 11, 2),  # x축 눈금 간격
            },
        )
        self.add(plane)

        # 함수 정의
        def func(x):
            return np.log(x + 1) + 0.1 * x

        # 함수 그래프 생성 - x_range 지정
        graph = plane.plot(
            func,
            x_range=[0, 10],
            color=RED,
            use_smoothing=True,
            dt=0.1,  # 포인트 간격을 더 작게 설정하여 부드럽게 표현
        )
        self.add(graph)

        # 함수 라벨 추가
        label = MathTex("f(x) = \\ln(x + 1) + 0.1x")
        label.to_edge(UP)
        self.add(label)


class CubicFunctionPlot(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={
                "color": BLUE,
                "numbers_to_include": np.arange(-3, 4, 1),
            },
        )
        self.add(plane)

        def cubic_func(x):
            return x**3 - 3 * x + 2

        graph = plane.plot(
            cubic_func,
            x_range=[-3, 3],
            color=RED,
            use_smoothing=True,
        )
        self.add(graph)

        label = MathTex("f(x) = x^3 - 3x + 2")
        label.to_edge(UP)
        self.add(label)


class ExponentialQuadraticPlot(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-2, 3, 1],
            y_range=[-5, 15, 2],
            x_length=6,
            y_length=6,
            axis_config={
                "color": BLUE,
                "numbers_to_include": np.arange(-2, 4, 1),
            },
        )
        self.add(plane)

        def exp_quad_func(x):
            return np.exp(x) - x**2

        graph = plane.plot(
            exp_quad_func,
            x_range=[-2, 3],
            color=RED,
            use_smoothing=True,
        )
        self.add(graph)

        label = MathTex("f(x) = e^x - x^2")
        label.to_edge(UP)
        self.add(label)
