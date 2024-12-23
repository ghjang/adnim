from manim import *

from .number_plane_group_base import (
    calculate_enough_number_of_samples,
    create_asymptote_lines,
    NumberPlaneGroupBase,
    MobjectType,
)


class FunctionPlotMixIn(NumberPlaneGroupBase):
    def __init__(self, **kwargs):
        if not hasattr(self, '_init_called'):
            super().__init__(**kwargs)
        self._ensure_single_init()

    def remove_function(self, name):
        """함수 그래프 제거"""
        graph = self.find_mobject(name, MobjectType.FUNCTION)
        if (graph):
            self.remove(graph)

    def get_function_graph(self, name):
        """특정 함수 그래프 가져오기"""
        return self.find_mobject(name, MobjectType.FUNCTION)

    def plot_parametric(self,
                        func,  # (t) -> (x,y) 형태의 함수
                        t_range=[0, 2*PI],
                        name=None,
                        color=BLUE,
                        stroke_width=2):
        """파라메트릭 함수 그래프 추가"""
        if name is None:
            name = f"parametric_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.PARAMETRIC])}"

        graph = self.plane.plot_parametric_curve(
            func,
            t_range=t_range,
            color=color,
            stroke_width=stroke_width
        )
        self._ensure_metadata(graph)
        graph.metadata = {"type": MobjectType.PARAMETRIC, "name": name}

        self.add(graph)
        return graph

    def plot_function(self,
                      func,
                      name=None,
                      x_range=None,
                      color=BLUE,
                      stroke_width=2,
                      **kwargs):  # 추가 인자를 받을 수 있도록 kwargs 추가
        """함수 그래프 추가"""
        if x_range is None:
            x_range = self.plane.x_range[:2]

        if name is None:
            name = f"function_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.FUNCTION])}"

        graph = self.plane.plot(
            func,
            x_range=x_range,
            color=color,
            stroke_width=stroke_width,
            **kwargs  # 추가 인자들을 plot 메서드로 전달
        )

        self._ensure_metadata(graph)
        graph.metadata = {
            "type": MobjectType.FUNCTION,
            "name": name,
            "base_plane": self.plane,  # 기준 평면 저장
            "x_range": x_range         # x_range 저장
        }

        self.add(graph)
        return graph

    def plot_discontinuous_function(
        self,
        func,                    # 실제 함수 (x -> y)
        x_range=None,           # x 범위
        # (x_min, x_max) -> [x1, x2, ...] 불연속점 계산 함수
        discontinuity_finder=None,
        epsilon=0.001,          # 불연속점 근처 제외 범위
        y_limit=None,           # y값 제한 (None이면 axes의 y범위 사용)
        y_margin_ratio=0.17,    # y축 범위에 대한 여유 공간 비율
        name=None,  # 이름 파라미터 추가
        color=BLUE,
        stroke_width=2,
        show_discontinuities=True,  # 불연속점 표시 여부
        discontinuity_config=None,  # 점근선 스타일 설정
        **kwargs
    ):
        """불연속 구간을 포함하는 함수 그래프 추가

        Args:
            func: 그릴 함수 (x -> y)
            x_range: x 범위. None이면 plane의 x_range 사용
            discontinuity_finder: 불연속점을 찾는 함수 (x_min, x_max) -> [불연속점들]
            epsilon: 불연속점 근처에서 제외할 범위
            y_limit: y값 제한
            y_margin_ratio: y축 범위에 대한 여유 공간 비율
            color: 그래프 색상
            stroke_width: 선 두께
            show_discontinuities: 불연속점 표시 여부
            discontinuity_config: 점근선 설정 (color, dash_length, stroke_width 등)
            **kwargs: plot_function에 전달할 추가 인자

        Returns:
            VGroup: (graph_segments, discontinuity_lines)
        """
        if x_range is None:
            x_range = self.plane.x_range[:2]

        if name is None:
            name = f"discontinuous_function_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.FUNCTION])}"

        if discontinuity_config is None:
            discontinuity_config = {
                "color": RED,
                "dash_length": 0.1,
                "stroke_width": 1.5
            }

        # 불연속점이 없으면 일반 plot_function 사용
        if discontinuity_finder is None:
            return self.plot_function(
                func,
                x_range=x_range,
                color=color,
                stroke_width=stroke_width,
                **kwargs
            )

        # 불연속점과 연속구간 계산
        discontinuities = discontinuity_finder(x_range[0], x_range[1])

        # 연속구간 계산
        ranges = []
        current = x_range[0]

        for x in discontinuities:
            if current < x - epsilon:
                ranges.append((current, x - epsilon))
            current = x + epsilon

        if current < x_range[1]:
            ranges.append((current, x_range[1]))

        # y값 제한 계산
        if y_limit is None:
            y_limit = max(abs(self.plane.y_range[0]), abs(
                self.plane.y_range[1]))
            y_margin = y_limit * y_margin_ratio
            y_limit += y_margin

        # 그래프 세그먼트 생성
        result_group = VGroup()

        # 메타데이터 설정
        self._ensure_metadata(result_group)
        result_group.metadata = {
            "type": MobjectType.FUNCTION,
            "name": name,
            "base_plane": self.plane,
            "x_range": x_range,
            "is_discontinuous": True,
            "discontinuities": discontinuity_finder(x_range[0], x_range[1]) if discontinuity_finder else None
        }

        num_samples = calculate_enough_number_of_samples(self.plane.x_length)

        # 연속구간별 그래프 생성
        graph_segments = VGroup()
        for x_min, x_max in ranges:
            segment = self._plot_function_segment(
                func, x_min, x_max, num_samples,
                y_limit, color, stroke_width, **kwargs
            )
            # 세그먼트도 메타데이터 포함
            self._ensure_metadata(segment)
            segment.metadata = {
                "type": MobjectType.FUNCTION,
                "parent_name": name,
                "x_range": [x_min, x_max]
            }
            graph_segments.add(segment)

        # 불연속점 표시
        if show_discontinuities and discontinuities:
            discontinuity_lines = create_asymptote_lines(
                self.plane,
                discontinuities,
                **discontinuity_config
            )
            # 점근선 그룹에 메타데이터 설정
            self._ensure_metadata(discontinuity_lines)
            discontinuity_lines.metadata = {
                "type": "ASYMPTOTES",
                "parent_name": name
            }
            result_group.add(discontinuity_lines)

        result_group.add(graph_segments)
        self.add(result_group)
        return result_group

    def _plot_function_segment(self, func, x_min, x_max, num_samples, y_limit, color, stroke_width, **kwargs):
        """함수의 한 구간을 그리는 헬퍼 메서드"""
        # 구간의 길이에 비례하여 샘플 수 계산
        total_range = self.plane.x_range[1] - self.plane.x_range[0]
        interval_length = x_max - x_min
        interval_samples = int(num_samples * (interval_length / total_range))
        interval_samples = max(interval_samples, 50)  # 최소 샘플 수 보장

        # 샘플링
        x_values = np.linspace(x_min, x_max, interval_samples)
        y_values = [func(x) for x in x_values]

        # y값 범위 제한
        mask = np.abs(y_values) <= y_limit
        x_values = x_values[mask]
        y_values = np.array(y_values)[mask]

        # 구간 그래프 생성
        return self.plane.plot_line_graph(
            x_values=x_values,
            y_values=y_values,
            line_color=color,
            stroke_width=stroke_width,
            vertex_dot_style={"fill_opacity": 0},
            **kwargs
        )
