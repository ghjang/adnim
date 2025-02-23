from manim import *
import numpy as np


class SoftmaxVisualization(Scene):
    def construct(self):
        # 타이틀 생성
        title = Text("Softmax Function Visualization", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 입력 벡터 생성 및 표시
        input_values = [2.0, 1.0, 0.1]
        input_tex = Tex(
            "Input: ", f"[{input_values[0]}, {input_values[1]}, {input_values[2]}]",
            font_size=36
        ).next_to(title, DOWN)

        # exponential 계산 과정
        exp_values = np.exp(input_values)
        exp_tex = Tex(
            "Exp: ", f"[{exp_values[0]:.2f}, {exp_values[1]:.2f}, {exp_values[2]:.2f}]",
            font_size=36
        ).next_to(input_tex, DOWN)

        # softmax 결과 계산
        softmax_values = exp_values / np.sum(exp_values)
        softmax_tex = Tex(
            "Softmax: ", f"[{softmax_values[0]:.2f}, {softmax_values[1]:.2f}, {softmax_values[2]:.2f}]",
            font_size=36
        ).next_to(exp_tex, DOWN)

        # 바 차트 생성
        bar_chart = BarChart(
            values=softmax_values,
            bar_names=["1", "2", "3"],
            y_range=[0, 1],
            y_axis_config={"font_size": 24},
            x_axis_config={"font_size": 24},
        ).scale(0.5)
        bar_chart.next_to(softmax_tex, DOWN, buff=1)

        # 애니메이션 실행
        self.play(Write(input_tex))
        self.wait()
        self.play(Write(exp_tex))
        self.wait()
        self.play(Write(softmax_tex))
        self.wait()
        self.play(Create(bar_chart))
        self.wait(2)
