from manim import *
from common.number_plane_group import *
from common.create_with_tracer import *
from common.sine_wave_components import *

# 상수 정의
MAIN_SCALE = 5
TRANSFORMED_SCALE = 1.1
FORMULA_SCALE = 0.8
INITIAL_ROTATION_TIME = 16    # 초기 1회전 시간
FINAL_ROTATION_TIME = 32      # 최종 4회전 시간 (8초/회전)
LEFT_EDGE_BUFF = 0.5
RIGHT_EDGE_BUFF = 0.5
N_COMPONENTS = 7              # 사인파 컴포넌트의 수
N_FINAL_REVOLUTIONS = 4       # 최종 회전 횟수

# 색상 테마 정의
COLOR_THEMES = {
    'PASTEL': {
        'CIRCLE_1': "#FF9ECD",  # 파스텔 핑크
        'CIRCLE_2': "#94C9FF",  # 파스텔 블루
        'CIRCLE_3': "#99FF99",  # 파스텔 그린
        'CIRCLE_4': "#FFB366",  # 파스텔 오렌지
        'CIRCLE_5': "#B19CD9",  # 파스텔 퍼플
        'CIRCLE_6': "#87CEEB",  # 스카이 블루
        'CIRCLE_7': "#FFB7B7",  # 라이트 코랄
        'VECTOR_1': "#FF9ECD",
        'VECTOR_2': "#94C9FF",
        'VECTOR_3': "#99FF99",
        'VECTOR_4': "#FFB366",
        'VECTOR_5': "#B19CD9",
        'VECTOR_6': "#87CEEB",
        'VECTOR_7': "#FFB7B7",
        'RESULT_VECTOR': YELLOW,
        'END_DOT': "#FF9ECD",
        'PLOT': RED
    },
    'NEON': {
        'CIRCLE_1': "#FF00FF",  # 네온 마젠타
        'CIRCLE_2': "#00FFFF",  # 네온 시안
        'CIRCLE_3': "#00FF00",  # 네온 그린
        'CIRCLE_4': "#FFFF00",  # 네온 옐로우
        'CIRCLE_5': "#FF00CC",  # 네온 핑크
        'CIRCLE_6': "#00CCFF",  # 네온 블루
        'CIRCLE_7': "#FF3333",  # 밝은 레드
        'VECTOR_1': "#FF00FF",
        'VECTOR_2': "#00FFFF",
        'VECTOR_3': "#00FF00",
        'VECTOR_4': "#FFFF00",
        'VECTOR_5': "#FF00CC",
        'VECTOR_6': "#00CCFF",
        'VECTOR_7': "#FF3333",
        'RESULT_VECTOR': YELLOW,
        'END_DOT': "#FF00FF",
        'PLOT': RED
    },
    'SUNSET': {  # 새로운 그라데이션 테마 추가
        'CIRCLE_1': "#FF5E62",  # 선홍색
        'CIRCLE_2': "#FF9966",  # 코럴
        'CIRCLE_3': "#FFAC68",  # 살몬
        'CIRCLE_4': "#FFB88C",  # 피치
        'CIRCLE_5': "#FFC3A0",  # 라이트 피치
        'CIRCLE_6': "#FFD4B2",  # 파스텔 피치
        'CIRCLE_7': "#FFE6CC",  # 크림
        'VECTOR_1': "#FF5E62",
        'VECTOR_2': "#FF9966",
        'VECTOR_3': "#FFAC68",
        'VECTOR_4': "#FFB88C",
        'VECTOR_5': "#FFC3A0",
        'VECTOR_6': "#FFD4B2",
        'VECTOR_7': "#FFE6CC",
        'RESULT_VECTOR': "#FF8E9E",  # 밝은 핑크
        'END_DOT': "#FF5E62",
        'PLOT': RED
    },
    'OCEAN_DEPTHS': {  # 새로운 그라데이션 테마
        'CIRCLE_1': "#00B5AD",  # 밝은 청록색 (가장 큰 원)
        'CIRCLE_2': "#2185D0",  # 밝은 파랑
        'CIRCLE_3': "#6435C9",  # 보라
        'CIRCLE_4': "#A333C8",  # 자주색
        'CIRCLE_5': "#E03997",  # 분홍
        'CIRCLE_6': "#B5297E",  # 진한 분홍
        'CIRCLE_7': "#7B1FA2",  # 깊은 보라 (가장 작은 원)
        'VECTOR_1': "#00B5AD",
        'VECTOR_2': "#2185D0",
        'VECTOR_3': "#6435C9",
        'VECTOR_4': "#A333C8",
        'VECTOR_5': "#E03997",
        'VECTOR_6': "#B5297E",
        'VECTOR_7': "#7B1FA2",
        'RESULT_VECTOR': "#00D1C1",  # 밝은 청록색
        'END_DOT': "#00B5AD",
        'PLOT': RED
    }
}

# 현재 사용할 테마 선택 (기본값: PASTEL)
CURRENT_THEME = 'PASTEL'
COLORS = COLOR_THEMES[CURRENT_THEME]


def create_formula(n_components: int = 3):
    """n개의 사인파 합 수식 생성

    Args:
        n_components: 사인파의 개수 (기본값: 3)
    """
    # 모든 항과 + 기호를 번갈아가며 리스트에 추가
    elements = []

    # 첫 번째 항 추가
    elements.append(r"\sin(x)")

    # 2번째 항부터 마지막 항까지 + 기호와 함께 추가
    for i in range(2, n_components + 1):
        elements.append("+")  # + 기호
        elements.append(r"\frac{\sin(" + str(i) + r"x)}{" + str(i) + r"}")  # 항

    # 색상 매핑 생성 (항만 색상 지정, + 기호는 제외)
    color_map = {}
    term_index = 0
    for i, elem in enumerate(elements):
        if elem != "+":  # + 기호가 아닌 경우에만 색상 매핑
            color_map[elem] = COLORS[f'VECTOR_{term_index + 1}']
            term_index += 1

    return MathTex(
        *elements,  # 항과 + 기호가 번갈아가며 나타남
        tex_to_color_map=color_map
    ).scale(FORMULA_SCALE)


def create_sum_function_with_amplitude(n: int = 3) -> callable:
    """n개의 진폭이 다른 사인파의 합 함수 생성

    Args:
        n: 합성할 사인파의 개수 (기본값: 3)

    Returns:
        x에 대한 n개 사인파의 합을 계산하는 함수
        각 k번째 사인파는 sin(kx)/k 형태
    """
    def sum_sine(x: float) -> float:
        return sum(np.sin(k * x) / k for k in range(1, n + 1))
    return sum_sine


class SawtoothWave(Scene):
    def construct(self):
        self.next_section(
            "Intro of Plotting a Sawtooth Wave",
            skip_animations=False
        )

        # Title with gradient color
        title = Text("Plotting a Sawtooth Wave", font_size=68)
        title.set_color_by_gradient(PURPLE_E, GREEN_E, PINK, YELLOW_E)
        self.play(FadeIn(title))
        self.wait()
        self.play(
            title.animate.to_edge(UP, buff=0.1).set_opacity(0),
            run_time=1
        )

        self.next_section("Initial Circles and Vectors", skip_animations=False)

        # 초기 좌표계 생성 및 표시
        npg = NumberPlaneGroup().scale(MAIN_SCALE)
        self.play(FadeIn(npg))

        # 회전 요소 관리자 생성
        manager = SineWaveManager(npg)

        # N_COMPONENTS개의 원과 벡터를 한 번에 생성
        prev_vector = None
        for i in range(N_COMPONENTS):
            if i == 0:
                # 첫 번째 원/벡터는 원점에 생성
                config = RotationConfig(
                    center_point=(0, 0),
                    angular_velocity=i + 1,
                    color=COLORS[f'CIRCLE_{i+1}'],
                    name_suffix=str(i)
                )
                circle, vector = manager.add_component(config)
            else:
                # 나머지는 이전 벡터의 끝점에 생성
                radius = 1/(i + 1)  # i번째 원의 반지름
                circle = npg.add_circle(
                    center_point=npg.plane.p2c(prev_vector.get_end()),
                    radius=radius,
                    color=COLORS[f'CIRCLE_{i+1}'],
                    stroke_width=2,
                    fill_opacity=0.1,
                    name=f"circle_{i}"
                )
                vector = create_radius_vector(
                    npg,
                    circle,
                    0,
                    COLORS[f'VECTOR_{i+1}'],
                    f"radius_vector_{i}"
                )
                manager.circles.append(circle)
                manager.vectors.append(vector)

            self.play(FadeIn(circle), FadeIn(vector))
            prev_vector = vector

        self.next_section("Rotating Circles and Vectors",
                          skip_animations=False)

        # 스케일 다운하기 전에 먼저 한 번 회전 (합벡터 포함)
        first_rotation = [
            *manager.create_animations(n_revolutions=1),
            manager.create_resultant_animation()
        ]

        # 더 극적인 효과를 위한 커스텀 rate 함수
        def custom_rate(t):
            # 앞부분(0-40%)은 천천히
            if (t < 0.4):
                return rate_functions.ease_in_sine(t * 2.5) * 0.4
            # 중간부분(40-60%)은 빠르게
            elif (t < 0.6):
                return 0.4 + (t - 0.4) * 3
            # 나머지는 다시 천천히
            else:
                return 0.6 + rate_functions.ease_out_sine((t - 0.6) * 2.5) * 0.4

        # 또는 wiggle과 ease_in_out_elastic의 조합
        def dramatic_rate(t):
            elastic = rate_functions.ease_in_out_elastic(t)
            wiggle = rate_functions.wiggle(t)
            return (elastic + wiggle) / 2

        for anim in first_rotation:
            anim.rate_func = double_smooth

        # 첫 번째 회전 애니메이션
        self.play(*first_rotation, run_time=INITIAL_ROTATION_TIME)

        self.next_section("Transformed Plane and Formula",
                          skip_animations=False)

        # 변환된 좌표계로 전환
        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        ).scale(TRANSFORMED_SCALE).to_edge(LEFT, buff=LEFT_EDGE_BUFF).shift(UP)
        self.play(ReplacementTransform(npg, new_npg))
        manager.update_plane(new_npg)

        # 수식 추가 - N_COMPONENTS 사용
        formula = create_formula(n_components=N_COMPONENTS)
        formula.to_edge(DOWN, buff=1)
        self.play(FadeIn(formula))

        # 플롯 좌표계 생성
        plot_npg = NumberPlaneGroup(
            x_range=[-1, 8 * PI, 1],  # x 범위 8π까지 확장
            y_range=[-2, 2, 1],  # y축 범위를 [-2, 2]로 조정 (진폭 감소)
            x_length=1 + 2 * PI,
            y_length=2 + 2,
        ).scale(TRANSFORMED_SCALE).to_edge(RIGHT, buff=RIGHT_EDGE_BUFF).shift(UP)
        self.play(FadeIn(plot_npg))

        self.next_section("Sine Wave Plot", skip_animations=False)

        # 사인 플롯 생성 - N_COMPONENTS 사용
        sine_plot = plot_npg.plot_function(
            create_sum_function_with_amplitude(n=N_COMPONENTS),
            x_range=[0, 8 * PI],  # x범위를 8π까지로 확장
            color=COLORS['PLOT']
        )

        # 애니메이션 실행 - 회전 횟수를 4회로 변경하고 런타임 증가
        animations = [
            *manager.create_animations(n_revolutions=N_FINAL_REVOLUTIONS),
            manager.create_resultant_animation(),
            CreateWithTracer(
                sine_plot,
                rate_func=linear,
                tracer_config={
                    "cross_lines": True,
                    "show_v_line": True,
                    "screen_fixed_lines": True,
                    "fixed_x_range": [-4*PI, 8*PI]  # 범위도 확장
                }
            )
        ]

        # 런타임을 32초로 증가 (8초/회전)
        self.play(*animations, run_time=FINAL_ROTATION_TIME)
        self.wait(2)
