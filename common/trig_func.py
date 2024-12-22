from manim import *


def calculate_tan_ranges(x_min, x_max, epsilon=0.001):
    """탄젠트 함수의 연속구간들과 불연속점들을 계산

    Args:
        x_min (float): x 범위의 시작값
        x_max (float): x 범위의 끝값
        epsilon (float): 불연속점으로부터의 간격

    Returns:
        tuple: (ranges, discontinuities)
            - ranges: [(시작점, 끝점), ...] 형태의 연속구간 리스트
            - discontinuities: [x1, x2, ...] 형태의 불연속점 리스트
    """
    # 불연속점들 계산
    n_min = int(np.floor((x_min * 2/PI - 1) / 2))
    n_max = int(np.ceil((x_max * 2/PI - 1) / 2))

    discontinuities = [(2 * n + 1) * PI / 2 for n in range(n_min, n_max + 1)
                       if x_min <= (2 * n + 1) * PI / 2 <= x_max]

    # 연속구간 계산
    ranges = []
    current = x_min

    for x in discontinuities:
        if current < x - epsilon:
            ranges.append((current, x - epsilon))
        current = x + epsilon

    # 마지막 구간 추가
    if current < x_max:
        ranges.append((current, x_max))

    return ranges, discontinuities


def create_tan_segments(axes, x_ranges, num_samples, y_limit=None, y_margin_ratio=0.17):
    """탄젠트 함수의 구간별 그래프 세그먼트들을 생성

    Args:
        axes: Manim Axes 객체
        x_ranges: [(x_min, x_max), ...] 형태의 구간 리스트
        num_samples: 전체 샘플링 포인트 수
        y_limit: y값의 절대값 제한 (None이면 axes의 y범위 사용)
        y_margin_ratio: y축 범위에 대한 여유 공간 비율 (기본값: 0.17)

    Returns:
        VGroup: 생성된 탄젠트 그래프 세그먼트들
    """
    if y_limit is None:
        y_limit = max(abs(axes.y_range[0]), abs(axes.y_range[1]))
        y_margin = y_limit * y_margin_ratio
        y_limit += y_margin

    tan_segments = VGroup()
    total_range = axes.x_range[1] - axes.x_range[0]

    for x_min, x_max in x_ranges:
        # 구간의 길이에 비례하여 샘플 수 계산
        interval_length = x_max - x_min
        interval_samples = int(num_samples * (interval_length / total_range))
        interval_samples = max(interval_samples, 50)  # 최소 샘플 수 보장

        # 각 구간에 대한 샘플링
        x_values = np.linspace(x_min, x_max, interval_samples)
        y_values = np.tan(x_values)

        # y값 범위 제한 (여유값 포함)
        mask = np.abs(y_values) <= y_limit
        x_values = x_values[mask]
        y_values = y_values[mask]

        # 구간별 그래프 생성
        segment = axes.plot_line_graph(
            x_values=x_values,
            y_values=y_values,
            line_color=YELLOW,
            vertex_dot_style={"fill_opacity": 0}
        )
        tan_segments.add(segment)

    return tan_segments
