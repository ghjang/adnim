from manim import *
from common.line_decoration import LineMarker


class LineMarkerTest(Scene):
    def construct(self):
        examples = [
            # [선분 끝점, 마커 수, 위치, 회전]
            # 첫 번째 행: 1,2,3개 마커
            [2.0, 1, [-4, 1.5, 0], 0],          # 수평선, 1개 마커
            [2.0, 2, [0, 1.5, 0], PI/6],        # 30도 회전, 2개 마커
            [2.0, 3, [4, 1.5, 0], -PI/6],       # -30도 회전, 3개 마커
            # 두 번째 행: 4,5,6개 마커
            [2.0, 4, [-4, -1.5, 0], PI/4],      # 45도 회전, 4개 마커
            [2.0, 5, [0, -1.5, 0], -PI/4],      # -45도 회전, 5개 마커
            [2.0, 6, [4, -1.5, 0], 0],          # 수평선, 6개 마커
        ]

        for length, marker_count, pos, rotation in examples:
            # 선분 생성 및 회전
            line = Line(ORIGIN, RIGHT * length)
            line.rotate(rotation)

            # 마커 생성
            markers = LineMarker(
                line,
                count=marker_count,
                stroke_width=1.5
            )

            # 그룹으로 만들고 위치 지정
            group = VGroup(line, markers)
            group.move_to(pos)

            self.add(group)
