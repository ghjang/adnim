from manim import *

from common.number_plane_group import *
from common.animation.create_with_tracer import *
from common.sine_wave_components import *

# 상수 정의
MAIN_SCALE = 4
TRANSFORMED_SCALE = 0.9
FORMULA_SCALE = 0.8
ANIMATION_RUN_TIME = 8
LEFT_EDGE_BUFF = 1.5
RIGHT_EDGE_BUFF = 1.5

# 색상 설정
COLORS = {
    'CIRCLE_1': BLUE,
    'CIRCLE_2': PURPLE,
    'VECTOR_1': TEAL,
    'VECTOR_2': PINK,
    'RESULT_VECTOR': YELLOW,
    'END_DOT': RED,
    'PLOT': RED
}


def create_main_plane():
    """메인 좌표계 생성"""
    return NumberPlaneGroup().scale(MAIN_SCALE)


def create_transformed_plane(npg):
    """변환된 좌표계 생성"""
    return npg.copy_with_transformed_plane(
        x_range=[-2, 2, 1],
        y_range=[-2, 2, 1],
        x_length=4,
        y_length=4
    ).scale(TRANSFORMED_SCALE).to_edge(LEFT, buff=LEFT_EDGE_BUFF)


def create_plot_plane():
    """플롯 좌표계 생성"""
    return NumberPlaneGroup(
        x_range=[-1, 2 * PI, 1],
        y_range=[-3, 3, 1],
        x_length=1 + 2 * PI,
        y_length=3 + 3,
    ).scale(TRANSFORMED_SCALE).to_edge(RIGHT, buff=RIGHT_EDGE_BUFF)


def create_formula():
    """수식 생성"""
    return MathTex(
        r"\sin(x)", "+", r"\sin(2x)",
        tex_to_color_map={
            r"\sin(x)": COLORS['VECTOR_1'],
            r"\sin(2x)": COLORS['VECTOR_2']
        }
    ).scale(FORMULA_SCALE)


class SumOfTwoSine(Scene):
    def construct(self):
        # 초기 설정
        configs = [
            RotationConfig(
                center_point=(0, 0),
                angular_velocity=1,
                circle_radius=1,
                color=COLORS['CIRCLE_1'],
                name_suffix="0"
            ),
            RotationConfig(
                center_point=(1, 0),
                angular_velocity=2,
                circle_radius=1,
                color=COLORS['CIRCLE_2'],
                name_suffix="1"
            )
        ]

        # 초기 좌표계 생성 및 표시
        npg = create_main_plane()
        self.play(FadeIn(npg))

        # 회전 요소 관리자 생성
        manager = SineWaveManager(npg)

        # 회전 요소들 생성 및 표시
        for config in configs:
            circle, vector = manager.add_component(config)
            self.play(FadeIn(circle), FadeIn(vector))

        # 변환된 좌표계로 전환
        new_npg = create_transformed_plane(npg)
        self.play(ReplacementTransform(npg, new_npg))

        # 좌표계 변경 후 매니저 업데이트
        manager.update_plane(new_npg)

        # 수식 추가
        formula = create_formula()
        formula.next_to(new_npg, DOWN, buff=0.5)
        self.play(FadeIn(formula))

        # 플롯 좌표계 생성
        plot_npg = create_plot_plane()
        self.play(FadeIn(plot_npg))

        # 사인 플롯 생성
        sine_plot = plot_npg.plot_function(
            create_sum_function(len(configs)),
            x_range=[0, 2 * PI],
            color=COLORS['PLOT']
        )

        # 애니메이션 실행
        animations = [
            *manager.create_animations(),
            manager.create_resultant_animation(),
            CreateWithTracer(
                sine_plot,
                rate_func=linear,
                tracer_config={
                    "cross_lines": True,
                    "show_v_line": True,
                    "screen_fixed_lines": True,
                    "fixed_x_range": [-4*PI, 4*PI]
                }
            )
        ]

        self.play(*animations, run_time=ANIMATION_RUN_TIME)
        self.wait(2)
