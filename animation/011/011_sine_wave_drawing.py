from manim import *
import numpy as np

from common.number_plane_group import *
from common.animation.create_with_tracer import *


class SineWaveDrawing(Scene):
    def create_plane_group(self, position):
        """좌표평면 생성 헬퍼 함수"""
        if position == "right":
            return NumberPlaneGroup(
                x_range=[-1, 4 * PI, 1],
                y_range=[-2, 2, 1],
                x_length=1 + 4 * PI,
                y_length=2 + 2,
            ).scale(0.75)
        else:  # "left"
            return NumberPlaneGroup(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                x_length=4,
                y_length=4,
            ).scale(0.75)

    def create_unit_circle(self, plane):
        """단위원 생성 헬퍼 함수"""
        return plane.add_circle(
            center_point=(0, 0),
            radius=1,
            color=BLUE,
            stroke_width=2,
            fill_opacity=0.1
        )

    def create_radius_vector(self, plane, initial_angle, color):
        """반지름 벡터 생성 헬퍼 함수"""
        # initial_angle: 0 for sine (pointing right), PI/2 for cosine (pointing up)
        x = np.cos(initial_angle)
        y = np.sin(initial_angle)
        return Vector(
            direction=plane.plane.c2p(x, y) - plane.plane.c2p(0, 0),
            color=color,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        ).shift(plane.plane.c2p(0, 0))

    def create_vertical_line(self, plane, initial_value, color):
        """수직선 생성 헬퍼 함수"""
        start = plane.plane.c2p(-0.5, 0)
        return Line(
            start=start,
            end=plane.plane.c2p(-0.5, initial_value),
            color=color,
            stroke_width=4
        )

    def create_horizontal_dashed(self,
                                 unit_plane,
                                 unit_vector,
                                 graph_plane,
                                 initial_value,
                                 color):
        """수평 점선 생성 헬퍼 함수"""

        # 화면 좌표값 => 논리 좌표값 변환
        unit_vector_end = unit_plane.plane.p2c(unit_vector.get_end())

        return DashedLine(
            start=unit_plane.plane.c2p(unit_vector_end[0], unit_vector_end[1]),
            end=graph_plane.plane.c2p(-0.5, initial_value),
            color=color,
            stroke_width=2,
            dash_length=0.025
        )

    def create_trig_system(self, initial_phase=0, color=RED):
        """삼각함수 시스템(단위원+그래프) 생성"""
        system = VGroup()

        # 평면들 생성 및 배치
        graph_plane = self.create_plane_group("right")
        unit_plane = self.create_plane_group("left")
        plane_group = VGroup(unit_plane, graph_plane).arrange(RIGHT, buff=0.7)
        system.add(plane_group)

        # 단위원 추가
        circle = self.create_unit_circle(unit_plane)
        system.add(circle)

        # 초기 위치의 좌표값 계산 (코사인은 초기값이 1이어야 함)
        x = np.cos(initial_phase)
        y = np.sin(initial_phase)
        initial_value = y
        projection_point = y

        # 벡터, 수직선, 점선 생성 및 추가
        vector = self.create_radius_vector(
            unit_plane,
            initial_phase,
            color
        )
        vertical = self.create_vertical_line(
            graph_plane,
            projection_point,
            color
        )
        dashed = self.create_horizontal_dashed(
            unit_plane,
            vector,
            graph_plane,
            projection_point,
            LIGHT_GRAY
        )

        system.add(vector, vertical, dashed)

        # 시스템에 메타데이터 추가
        system.metadata = {
            "graph_plane": graph_plane,
            "unit_plane": unit_plane,
            "vector": vector,
            "vertical": vertical,
            "dashed": dashed
        }

        return system

    def construct(self):
        self.next_section("Initial Setup", skip_animations=False)

        # 사인 시스템 생성 (초기 위상 0)
        sine_system = self.create_trig_system(
            initial_phase=0,
            color=RED
        )
        sin_vector = sine_system.metadata["vector"]
        sin_vertical = sine_system.metadata["vertical"]
        sin_dashed = sine_system.metadata["dashed"]
        sin_graph_plane = sine_system.metadata["graph_plane"]

        # 코사인 시스템 생성 (초기 위상 PI/2)
        cosine_system = self.create_trig_system(
            initial_phase=PI/2,
            color=GREEN
        )
        cos_vector = cosine_system.metadata["vector"]
        cos_vertical = cosine_system.metadata["vertical"]
        cos_dashed = cosine_system.metadata["dashed"]
        cos_graph_plane = cosine_system.metadata["graph_plane"]

        # 전체 시스템을 2행 1열로 배치
        all_systems = VGroup(sine_system, cosine_system).arrange(
            DOWN,
            buff=0.75,
            center=True
        ).move_to(ORIGIN).shift(UP * 0.25)

        # 라벨 추가 및 위치 조정
        sine_label = MathTex(
            r"\sin(x)",
            color=RED,
            font_size=24
        ).next_to(
            sine_system.metadata["unit_plane"],  # 단위원 기준
            DOWN,
            buff=0.1
        )
        sine_system.add(sine_label)

        cosine_label = MathTex(
            r"\cos(x) = \sin(x + \frac{\pi}{2})",  # 위상차 관계식 추가
            color=GREEN,
            font_size=24
        ).next_to(
            cosine_system.metadata["unit_plane"],  # 단위원 기준
            DOWN,
            buff=0.1
        )
        cosine_system.add(cosine_label)

        self.add(all_systems)
        self.wait(2)

        self.next_section("Sine and Cosine Waves", skip_animations=False)

        def get_angle_point(angle):
            return np.cos(angle), np.sin(angle)

        def update_all(mob, alpha):
            current_angle = 4 * PI * alpha
            x, y = get_angle_point(current_angle)

            # 사인 업데이트
            sine_unit_plane = sine_system.metadata["unit_plane"]
            sin_end = sine_unit_plane.plane.c2p(x, y)
            sin_start = sine_unit_plane.plane.c2p(0, 0)

            sin_vector.become(
                Vector(
                    direction=sin_end - sin_start,
                    color=RED,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.15
                ).shift(sin_start)
            )
            sin_vertical.become(
                self.create_vertical_line(sin_graph_plane, y, RED))
            sin_dashed.become(
                DashedLine(
                    start=sin_end,
                    end=sin_graph_plane.plane.c2p(-0.5, y),
                    color=LIGHT_GRAY,
                    stroke_width=2,
                    dash_length=0.025
                )
            )

            # 코사인 업데이트 (90도 위상차)
            x_cos, y_cos = get_angle_point(current_angle + PI/2)
            cosine_unit_plane = cosine_system.metadata["unit_plane"]
            cos_end = cosine_unit_plane.plane.c2p(x_cos, y_cos)
            cos_start = cosine_unit_plane.plane.c2p(0, 0)

            cos_vector.become(
                Vector(
                    direction=cos_end - cos_start,
                    color=GREEN,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.15
                ).shift(cos_start)
            )
            cos_vertical.become(self.create_vertical_line(
                cos_graph_plane, x, GREEN))
            cos_dashed.become(
                DashedLine(
                    start=cos_end,
                    end=cos_graph_plane.plane.c2p(-0.5, x),
                    color=LIGHT_GRAY,
                    stroke_width=2,
                    dash_length=0.025
                )
            )

        # 그래프 생성 및 메타데이터 설정
        sine_plot = sin_graph_plane.plot_function(
            lambda x: np.sin(x),
            x_range=[0, 4 * PI],
            color=RED
        )
        sine_system.add(sine_plot)

        cosine_plot = cos_graph_plane.plot_function(
            lambda x: np.cos(x),
            x_range=[0, 4 * PI],
            color=GREEN
        )
        cosine_system.add(cosine_plot)

        self.play(
            CreateWithTracer(sine_plot, rate_func=linear, tracer_config={
                "cross_lines": True,
                "show_v_line": True,
                "screen_fixed_lines": True,
                "fixed_x_range": [-2.8, 8]
            }),
            CreateWithTracer(cosine_plot, rate_func=linear, tracer_config={
                "cross_lines": True,
                "show_v_line": False,
                "screen_fixed_lines": True,
                "fixed_x_range": [-2.8, 8]
            }),
            UpdateFromAlphaFunc(
                VGroup(
                    sin_vector,
                    sin_vertical,
                    sin_dashed,
                    cos_vector,
                    cos_vertical,
                    cos_dashed
                ),
                update_all,
                rate_func=linear
            ),
            run_time=5
        )

        self.wait(2)
