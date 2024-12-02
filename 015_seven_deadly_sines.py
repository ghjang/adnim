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

        # 세 번째 원과 벡터 생성 (반지름 1/3인 원)
        circle_2 = npg.add_circle(
            center_point=npg.plane.p2c(vector_1.get_end()),
            radius=1/3,  # 세 번째 원의 반지름
            color=COLORS['CIRCLE_3'],  # 수정
            stroke_width=2,
            fill_opacity=0.1,
            name="circle_2"
        )
        vector_2 = create_radius_vector(
            npg,
            circle_2,
            0,
            COLORS['VECTOR_3'],  # 수정
            "radius_vector_2"
        )
        self.play(FadeIn(circle_2), FadeIn(vector_2))
        manager.circles.append(circle_2)
        manager.vectors.append(vector_2)

        # 4번째에서 7번째 원과 벡터 생성
        for i in range(4, 8):
            prev_vector = manager.vectors[-1]  # 이전 벡터
            radius = 1/i  # i번째 원의 반지름
            circle = npg.add_circle(
                center_point=npg.plane.p2c(prev_vector.get_end()),
                radius=radius,
                color=COLORS[f'CIRCLE_{i}'],
                stroke_width=2,
                fill_opacity=0.1,
                name=f"circle_{i-1}"
            )
            vector = create_radius_vector(
                npg,
                circle,
                0,
                COLORS[f'VECTOR_{i}'],
                f"radius_vector_{i-1}"
            )
            self.play(FadeIn(circle), FadeIn(vector))
            manager.circles.append(circle)
            manager.vectors.append(vector)

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
        formula = create_formula(n_components=7)
        formula.to_edge(DOWN)
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
            create_sum_function_with_amplitude(n=7),
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
