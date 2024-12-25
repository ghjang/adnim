from manim import *
from common.number_plane_group import *
from common.create_with_tracer import *
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


def create_formula():
    """수식 생성: sin(x) + sin(2x)/2"""
    return MathTex(
        r"\sin(x)", "+", r"\frac{\sin(2x)}{2}",
        tex_to_color_map={
            r"\sin(x)": COLORS['VECTOR_1'],
            r"\frac{\sin(2x)}{2}": COLORS['VECTOR_2']
        }
    ).scale(FORMULA_SCALE)


def create_sum_function_with_amplitude() -> callable:
    """진폭이 다른 사인파의 합 함수 생성"""
    def sum_sine(x: float) -> float:
        return np.sin(x) + np.sin(2 * x) / 2
    return sum_sine


class SineWithHalfAmplitude(Scene):
    def construct(self):
        # 초기 설정 - 첫 번째 원/벡터 생성
        configs = [
            RotationConfig(
                center_point=(0, 0),
                angular_velocity=1,
                color=COLORS['CIRCLE_1'],
                name_suffix="0"
            )
        ]

        # 초기 좌표계 생성 및 표시
        npg = NumberPlaneGroup().scale(MAIN_SCALE)
        self.play(FadeIn(npg))

        # 회전 요소 관리자 생성
        manager = SineWaveManager(npg)

        # 첫 번째 원과 벡터 생성
        circle_0, vector_0 = manager.add_component(configs[0])
        self.play(FadeIn(circle_0), FadeIn(vector_0))

        # 두 번째 원과 벡터 생성 (반지름 0.5인 원)
        # 첫 번째 벡터의 끝점을 두 번째 원의 중심으로 사용
        circle_1 = npg.add_circle(
            center_point=npg.plane.p2c(vector_0.get_end()),
            radius=0.5,  # 이 크기로 벡터도 생성될 것입니다
            color=COLORS['CIRCLE_2'],
            stroke_width=2,
            fill_opacity=0.1,
            name="circle_1"
        )
        vector_1 = create_radius_vector(
            npg,
            circle_1,  # circle_1의 반지름(0.5)을 기준으로 벡터가 생성됨
            0,
            COLORS['VECTOR_2'],
            "radius_vector_1"
        )
        self.play(FadeIn(circle_1), FadeIn(vector_1))
        manager.circles.append(circle_1)
        manager.vectors.append(vector_1)

        # 변환된 좌표계로 전환
        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        ).scale(TRANSFORMED_SCALE).to_edge(LEFT, buff=LEFT_EDGE_BUFF)
        self.play(ReplacementTransform(npg, new_npg))
        manager.update_plane(new_npg)

        # 수식 추가
        formula = create_formula()
        formula.next_to(new_npg, DOWN, buff=0.5)
        self.play(FadeIn(formula))

        # 플롯 좌표계 생성
        plot_npg = NumberPlaneGroup(
            x_range=[-1, 2 * PI, 1],
            y_range=[-2, 2, 1],  # y축 범위를 [-2, 2]로 조정 (진폭 감소)
            x_length=1 + 2 * PI,
            y_length=2 + 2,
        ).scale(TRANSFORMED_SCALE).to_edge(RIGHT, buff=RIGHT_EDGE_BUFF)
        self.play(FadeIn(plot_npg))

        # 사인 플롯 생성
        sine_plot = plot_npg.plot_function(
            create_sum_function_with_amplitude(),
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
