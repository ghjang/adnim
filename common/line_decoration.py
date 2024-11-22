from manim import *


class LineMarker(VMobject):
    def __init__(
        self,
        line: Line,
        length: float = 0.15,
        color: str = YELLOW,
        count: int = 1,
        spacing: float = 0.1,  # 마커 간 간격 축소
        stroke_width: float = 2,
        **kwargs
    ):
        super().__init__(**kwargs)

        # 선분의 시작점과 방향 벡터 계산
        start = line.get_start()
        end = line.get_end()
        vector = end - start
        line_length = np.linalg.norm(vector)
        unit_vector = vector / line_length

        # 수직 벡터 계산 (z축 기준 90도 회전)
        perp_vector = np.array([-unit_vector[1], unit_vector[0], 0])

        # 마커 위치 계산 (중점 기준)
        mid_point = start + vector * 0.5
        if count == 1:
            positions = [0]  # 중점에 하나
        else:
            if count % 2 == 1:  # 홀수 개수
                positions = [
                    spacing * (i - (count-1)/2)
                    for i in range(count)
                ]
            else:  # 짝수 개수
                positions = [
                    spacing * (i - (count/2 - 0.5))
                    for i in range(count)
                ]

        # 각 위치에 마커 생성
        half_length = length / 2
        for offset in positions:
            marker_center = mid_point + offset * unit_vector
            marker = Line(
                marker_center - half_length * perp_vector,
                marker_center + half_length * perp_vector,
                color=color,
                stroke_width=stroke_width
            )
            self.add(marker)
