from manim import *
from enum import Enum, auto


class OriginStyle(Enum):
    DOT = auto()
    CIRCLE = auto()
    CROSS = auto()


class EnhancedNumberPlane(VGroup):
    def __init__(
        self,
        x_range=[-20, 20, 1],
        y_range=[-20, 20, 1],
        x_length=16,
        y_length=16,
        background_line_style={"stroke_opacity": 0.6},
        origin_style_type=OriginStyle.DOT,  # 기본값은 DOT
        origin_config={
            "color": RED,
            "size": 0.1,
            "opacity": 1.0
        },
        **kwargs
    ):
        super().__init__(**kwargs)

        # NumberPlane 생성
        self.plane = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            background_line_style=background_line_style
        )
        self.add(self.plane)

        # 원점 표시 생성
        self.origin_marker = self._create_origin_marker(
            origin_style_type, origin_config)
        self.add(self.origin_marker)

        self.current_style = origin_style_type

        # 함수 그래프들을 저장할 딕셔너리 추가
        self.function_graphs = {}

    def _create_origin_marker(self, style_type, config):
        """원점 표시 생성 헬퍼 메서드"""
        color = config.get("color", RED)
        size = config.get("size", 0.1)
        opacity = config.get("opacity", 1.0)

        # 원점 마커를 plane의 원점 위치에 생성
        origin_point = self.plane.c2p(0, 0)  # 좌표계의 (0,0)을 화면 좌표로 변환

        if style_type == OriginStyle.DOT:
            return Dot(
                point=origin_point,
                radius=size,  # size를 radius로 사용
                color=color
            ).set_opacity(opacity)
        elif style_type == OriginStyle.CIRCLE:
            return Circle(
                radius=size,
                color=color,
                fill_opacity=opacity
            ).move_to(origin_point)
        elif style_type == OriginStyle.CROSS:
            return VGroup(
                Line(UP * size, DOWN * size, color=color),
                Line(LEFT * size, RIGHT * size, color=color)
            ).move_to(origin_point).set_opacity(opacity)

    def set_origin_style(self, style_type, config=None):
        """원점 표시 스타일 변경"""
        if config is None:
            config = {
                "color": RED,
                "size": 0.1,
                "opacity": 1.0
            }

        # 기존 원점 표시 제거
        self.remove(self.origin_marker)

        # 새로운 원점 표시 생성 및 추가
        self.origin_marker = self._create_origin_marker(style_type, config)
        self.add(self.origin_marker)
        self.current_style = style_type

    # 원점 위치 업데이트를 위한 새로운 메서드 추가
    def update_origin_marker_position(self):
        """NumberPlane의 실제 원점 위치로 마커 업데이트"""
        origin_point = self.plane.c2p(0, 0)
        self.origin_marker.move_to(origin_point)

    # 기존 변환 메서드들을 오버라이드하여 원점 마커 위치 동기화
    def scale(self, scale_factor, **kwargs):
        super().scale(scale_factor, **kwargs)
        self.update_origin_marker_position()
        return self

    def shift(self, vector):
        super().shift(vector)
        self.update_origin_marker_position()
        return self

    def rotate(self, angle, **kwargs):
        super().rotate(angle, **kwargs)
        self.update_origin_marker_position()
        return self

    def hide_origin(self):
        """원점 표시 숨기기"""
        self.origin_marker.set_opacity(0)

    def show_origin(self):
        """원점 표시 보이기"""
        self.origin_marker.set_opacity(1)

    def plot_function(self,
                      func,
                      name=None,
                      x_range=None,
                      color=BLUE,
                      stroke_width=2):
        """함수 그래프 추가"""
        if x_range is None:
            x_range = self.plane.x_range[:2]  # min, max 값만 사용

        if name is None:
            name = f"function_{len(self.function_graphs)}"

        graph = self.plane.plot(
            func,
            x_range=x_range,
            color=color,
            stroke_width=stroke_width
        )

        self.function_graphs[name] = graph
        self.add(graph)
        return graph

    def remove_function(self, name):
        """함수 그래프 제거"""
        if name in self.function_graphs:
            graph = self.function_graphs.pop(name)
            self.remove(graph)

    def get_function_graph(self, name):
        """특정 함수 그래프 가져오기"""
        return self.function_graphs.get(name)

    def plot_parametric(self,
                       func,  # (t) -> (x,y) 형태의 함수
                       t_range=[0, 2*PI],
                       name=None,
                       color=BLUE,
                       stroke_width=2):
        """파라메트릭 함수 그래프 추가"""
        if name is None:
            name = f"parametric_{len(self.function_graphs)}"

        graph = self.plane.plot_parametric_curve(
            func,
            t_range=t_range,
            color=color,
            stroke_width=stroke_width
        )

        self.function_graphs[name] = graph
        self.add(graph)
        return graph
