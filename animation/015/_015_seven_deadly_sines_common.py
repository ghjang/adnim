from typing import override
from abc import ABC, abstractmethod
from manim import *

from common.number_plane_group import *
from common.animation.create_with_tracer import CreateWithTracer
from common.sine_wave_components import *
from _015_seven_deadly_sines_theme import COLOR_THEMES

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

# 현재 사용할 테마 선택 (기본값: PASTEL)
CURRENT_THEME = 'PASTEL'
COLORS = COLOR_THEMES[CURRENT_THEME]


class CompositeHarmonicScene(ZoomedScene, ABC):
    """여러 고조파의 합성을 보여주는 기본 클래스"""

    def __init__(
        self,
        n_components=3,
        main_scale=5,               # 초기 원들 홀로 회전하는 애니메이션에서의 좌표계 크기
        transformed_scale=0.9,      # 원들과 그래프 플랏 좌표계들 크기
        formula_scale=0.8,
        animation_run_time=8,
        initial_rotation_run_time=16,
        final_rotation_run_time=32,
        left_edge_buff=0.5,
        right_edge_buff=0.5,
        bottom_edge_buff=1,
        color_theme='PASTEL',
        **kwargs
    ):
        super().__init__(**kwargs)

        self.n_components = n_components
        self.main_scale = main_scale
        self.transformed_scale = transformed_scale
        self.formula_scale = formula_scale
        self.animation_run_time = animation_run_time
        self.initial_rotation_time = initial_rotation_run_time
        self.final_rotation_time = final_rotation_run_time
        self.left_edge_buff = left_edge_buff
        self.right_edge_buff = right_edge_buff
        self.bottom_edge_buff = bottom_edge_buff
        self.colors = COLOR_THEMES[color_theme]

    @abstractmethod
    def create_title(self):
        pass

    def before_initial_rotation(self, sine_wave_manager):
        pass

    def initial_rotation_update(self, sine_wave_manager, alpha):
        pass

    def after_initial_rotation(self, sine_wave_manager):
        pass

    @abstractmethod
    def create_formula_latex(self):
        pass

    @abstractmethod
    def create_graph_plot_function(self):
        pass

    @abstractmethod
    def create_circle_rotation_info(self, component_index):
        pass

    def create_plot_plane_config(self):
        """플롯 좌표계 설정을 반환하는 메서드 (오버라이드 가능)"""
        return {
            'x_range': [-1, 8 * PI, 1],
            'y_range': [-2, 2, 1],
            'x_length': 1 + 2.8 * PI,
            'y_length': 2 + 2,
        }

    def get_component_config(self, npg, component_index, prev_vector=None):
        """각 컴포넌트의 설정 반환"""

        circle_radius, angular_velocity = self.create_circle_rotation_info(
            component_index
        )

        if prev_vector:
            center_point = npg.plane.p2c(prev_vector.get_end())
        else:
            center_point = (0, 0)

        return RotationConfig(
            center_point=center_point,
            angular_velocity=angular_velocity,
            circle_radius=circle_radius,
            color=self.colors[f'CIRCLE_{component_index+1}'],
            name_suffix=str(component_index)
        )

    @override
    def construct(self):
        """메인 애니메이션 시퀀스"""

        self.next_section("Show title", skip_animations=False)

        # 타이틀 표시 (있는 경우)
        title = self.create_title()
        if (title):
            self.play(FadeIn(title))
            self.wait()
            self.play(title.animate.to_edge(UP, buff=0.1).set_opacity(0))

        self.next_section("Setup main plane", skip_animations=False)

        # 초기 좌표계 생성
        npg = NumberPlaneGroup().scale(self.main_scale)
        self.play(FadeIn(npg))

        # 회전 요소 관리자 생성
        manager = SineWaveManager(npg)

        self.next_section("Add components", skip_animations=False)

        # 컴포넌트 생성
        prev_vector = None
        for i in range(self.n_components):
            config = self.get_component_config(npg, i, prev_vector)
            circle, vector = manager.add_component(config)
            self.play(FadeIn(circle), FadeIn(vector))
            prev_vector = vector

        self.next_section("Initial rotation", skip_animations=False)
        self.before_initial_rotation(manager)

        # 초기 1회전
        first_rotation = [
            *manager.create_animations(n_revolutions=1),
            manager.create_resultant_animation()
        ]

        for anim in first_rotation:
            anim.rate_func = double_smooth

        self.play(
            *first_rotation,
            UpdateFromAlphaFunc(
                Mobject(),
                update_function=lambda _, alpha: self.initial_rotation_update(
                    manager, alpha)
            ),
            run_time=self.initial_rotation_time
        )
        self.after_initial_rotation(manager)

        self.next_section("Transform to new coordinate system",
                          skip_animations=False)
        # 변환된 좌표계로 전환
        new_npg = npg.copy_with_transformed_plane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        ).scale(self.transformed_scale).to_edge(LEFT, buff=self.left_edge_buff).shift(UP)

        self.play(ReplacementTransform(npg, new_npg))
        manager.update_plane(new_npg)

        self.next_section("Show formula", skip_animations=False)

        # 수식 추가
        formula = self.create_formula_latex()
        formula.scale(self.formula_scale)
        formula.to_edge(DOWN, buff=self.bottom_edge_buff)
        self.play(FadeIn(formula))

        self.next_section("Setup plot plane", skip_animations=False)

        # 플롯 좌표계 생성
        plot_config = self.create_plot_plane_config()
        plot_npg = NumberPlaneGroup(**plot_config)\
            .scale(self.transformed_scale)\
            .to_edge(RIGHT, buff=self.right_edge_buff)\
            .shift(UP)

        self.play(FadeIn(plot_npg))

        self.next_section("Final animation", skip_animations=False)

        plot_config = self.create_plot_plane_config()

        # 플롯의 x축 범위에 따라 필요한 회전 수 계산
        # x축 범위가 2π마다 1회전이므로, 전체 범위를 2π로 나누면 필요한 회전 수가 됨.
        x_range = plot_config['x_range']
        total_x_range = x_range[1]                     # '0'부터 시작하므로
        n_revolutions = int(total_x_range / (2 * PI))  # 2π당 1회전

        # 최종 애니메이션
        sine_plot = plot_npg.plot_function(
            self.create_graph_plot_function(),
            x_range=[0, total_x_range],
            color=self.colors['PLOT']
        )

        animations = [
            *manager.create_animations(n_revolutions=n_revolutions),
            manager.create_resultant_animation(),
            CreateWithTracer(
                sine_plot,
                rate_func=linear,
                tracer_config={
                    "cross_lines": True,
                    "show_v_line": True,
                    "screen_fixed_lines": True,
                    "fixed_x_range": [-4*PI, 8*PI]
                }
            )
        ]

        self.play(*animations, run_time=self.final_rotation_time)
        self.wait(2)
