from manim import *
from common.number_plane_group import *
from common.animation.create_with_tracer import CreateWithTracer


class SinePlot(Scene):
    def construct(self):
        plane_group = NumberPlaneGroup().scale(2)
        self.add(plane_group)

        # 사인 함수 그래프 추가
        sine_plot = plane_group.plot_function(
            lambda x: np.sin(x),
            x_range=[-2 * PI * 2, 2 * PI * 2],
            color=BLUE
        )
        self.play(Create(sine_plot), run_time=6)


class CosinePlot(Scene):
    def construct(self):
        plane_group = NumberPlaneGroup().scale(2)
        self.add(plane_group)

        # 사인 함수 그래프 추가
        cosine_plot = plane_group.plot_function(
            lambda x: np.cos(x),
            x_range=[-2 * PI * 2, 2 * PI * 2],
            color=BLUE
        )
        self.play(Create(cosine_plot), run_time=6)


def tan_discontinuity_finder(x_min, x_max):
    """탄젠트 함수의 불연속점 계산"""
    n_min = int(np.floor((x_min * 2/PI - 1) / 2))
    n_max = int(np.ceil((x_max * 2/PI - 1) / 2))
    return [(2 * n + 1) * PI / 2 for n in range(n_min, n_max + 1)
            if x_min <= (2 * n + 1) * PI / 2 <= x_max]


class TangentPlot(Scene):
    def construct(self):
        plane_group = NumberPlaneGroup().scale(2)
        self.add(plane_group)

        # 탄젠트 함수 그래프 추가 (불연속점 자동 처리)
        tangent_graph = plane_group.plot_discontinuous_function(
            func=np.tan,
            x_range=[-3 * PI, 3 * PI],
            discontinuity_finder=tan_discontinuity_finder,
            color=BLUE,
        )

        self.play(Create(tangent_graph), run_time=6)


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

        t = ValueTracker(-2 * PI * 2)  # 시작점

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
            x_range=[-2 * PI * 2, 2 * PI * 2],
            color=BLUE
        )

        # 그래프를 그리면서 점이 따라다니는 애니메이션
        self.play(
            Create(sine_plot),
            t.animate.set_value(2 * PI * 2),
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
