from manim import *
from common.number_plane_group import *
from common.create_with_tracer import CreateWithTracer


class SinePlot(Scene):
    def construct(self):
        plane_group = NumberPlaneGroup().scale(2)
        self.add(plane_group)

        # 사인 함수 그래프 추가
        sine_plot = plane_group.plot_function(
            lambda x: np.sin(x),
            x_range=[-2*PI*2, 2*PI*2],
            color=BLUE
        )
        self.play(Create(sine_plot), run_time=6)


class SinePlotWithTracer(Scene):
    def construct(self):
        plane_group = NumberPlaneGroup().scale(2)
        self.add(plane_group)

        # 추적점 생성
        tracer = Dot(color=RED)
        self.add(tracer)

        # 사인 함수 그래프와 추적점 애니메이션
        def sine_func(x):
            return np.sin(x)

        t = ValueTracker(-2*PI*2)  # 시작점

        # 추적점의 위치를 업데이트하는 함수
        tracer.add_updater(
            lambda m: m.move_to(
                plane_group.plane.c2p(
                    t.get_value(),
                    sine_func(t.get_value())
                )
            )
        )

        # 사인 함수 그래프 생성 애니메이션
        sine_plot = plane_group.plot_function(
            sine_func,
            x_range=[-2*PI*2, 2*PI*2],
            color=BLUE
        )

        # 그래프를 그리면서 점이 따라다니는 애니메이션
        self.play(
            Create(sine_plot),
            t.animate.set_value(2*PI*2),
            run_time=6
        )

        # 추적점이 사라지는 애니메이션
        self.play(FadeOut(tracer))


class SinePlotWithCustomTracer(Scene):
    def construct(self):
        plane_group = NumberPlaneGroup(
            origin_config={
                "style": OriginStyle.CROSS,
            }
        ).scale(2).shift(RIGHT*2)
        self.add(plane_group)

        sine_plot = plane_group.plot_function(
            lambda x: np.sin(x),
            x_range=[-2*PI*2, 2*PI*2],
            color=BLUE
        )

        # 화면 고정 좌표 모드 사용 예시
        self.play(
            CreateWithTracer(
                sine_plot,
                rate_func=linear,
                tracer_config={
                    "color": RED,
                    "radius": 0.08,
                    "cross_lines": True,
                    "show_v_line": False,
                    "screen_fixed_lines": True,
                    "fixed_x_range": [-1, 8]
                },
                run_time=6
            )
        )
