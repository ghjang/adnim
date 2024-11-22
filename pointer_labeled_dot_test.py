from manim import *
from common.pointer_labeled_dot import PointerLabeledDot


class PointerLabeledDotExample(Scene):
    def construct(self):
        self.next_section("PointerLabeledDot 단순 예제", skip_animations=False)

        dot1 = PointerLabeledDot(
            label_text="A",
            dot_radius=0.2,
            pointer_length=1.5,
            label_font_size=36
        )
        self.play(Create(dot1))
        self.wait(2)
        self.play(FadeOut(dot1))

        self.next_section("PointerLabeledDot 이동 예시")

        # dot2 생성 및 통합 변경 테스트
        dot2 = PointerLabeledDot(
            label_text="START",
            pointer_direction=DR,
            dot_color=BLUE,
            arrow_color=YELLOW,
            label_color=GREEN
        )
        self.play(Create(dot2))
        self.wait(1)

        # 위치와 방향 변경 시퀀스 (시계방향으로 8방향 순회하며 안쪽으로)
        moves = [
            ((UP + LEFT) * 2,    UL, "UL"),     # 좌상단
            (UP * 2,            UP, "UP"),      # 상단
            ((UP + RIGHT) * 2,  UR, "UR"),     # 우상단
            (RIGHT * 2,         RIGHT, "R"),    # 우측
            ((DOWN + RIGHT) * 2, DR, "DR"),     # 우하단
            (DOWN * 2,          DOWN, "D"),     # 하단
            ((DOWN + LEFT) * 2, DL, "DL"),     # 좌하단
            (LEFT * 2,          LEFT, "L"),     # 좌측
            (ORIGIN,            DR, "CENTER")   # 중앙으로 복귀
        ]

        # 각 위치로 이동하면서 방향과 텍스트도 함께 변경
        for pos, direction, text in moves:
            # 1단계: 위치/방향만 변경된 상태로 변환
            new_dot = dot2.copy_and_change(
                new_point=pos,
                new_direction=direction,
                new_label_text=text
            )

            self.play(
                ReplacementTransform(dot2, new_dot),
                run_time=0.8
            )
            dot2 = new_dot


class PointerLabeledDotExample1(Scene):
    def construct(self):
        # 8방향 정의
        directions = {
            "UL": (UP + LEFT, UL),    "U": (UP, UP),       "UR": (UP + RIGHT, UR),
            "L":  (LEFT, LEFT),                             "R":  (RIGHT, RIGHT),
            "DL": (DOWN + LEFT, DL),   "D": (DOWN, DOWN),   "DR": (DOWN + RIGHT, DR)
        }

        # 공통 설정
        GRID_SCALE = 1.8  # 그리드 전체 크기
        TITLE_BUFF = 0.6  # 타���틀과 그리드 사이 간격
        GRID_SHIFT = 3.5  # 좌우 그리드 간격

        # 왼쪽 그리드 (안에서 밖으로)
        outward_dots = VGroup()
        for label, (pos, direction) in directions.items():
            dot = PointerLabeledDot(
                point=pos*GRID_SCALE,
                label_text=label,
                pointer_direction=direction,
                pointer_length=0.6,  # 화살표 길이 조정
                dot_color=BLUE,
                arrow_color=YELLOW,
                label_color=GREEN,
                label_font_size=24
            )
            outward_dots.add(dot)
        outward_dots.shift(LEFT*GRID_SHIFT)

        # 오른쪽 그리드 (밖에서 안으로)
        inward_dots = VGroup()
        for label, (pos, direction) in directions.items():
            dot = PointerLabeledDot(
                point=pos*GRID_SCALE,
                label_text=label,
                pointer_direction=-direction,
                pointer_length=0.6,  # 화살표 길이 조정
                dot_color=RED,
                arrow_color=BLUE,
                label_color=YELLOW,
                label_font_size=24
            )
            inward_dots.add(dot)
        inward_dots.shift(RIGHT*GRID_SHIFT)

        # 제목 추가 (동일한 높이에 배치)
        title_style = {"font_size": 36}
        title_out = Text("Outward", color=WHITE, **title_style)
        title_in = Text("Inward", color=WHITE, **title_style)

        # 제목 위치 조정 (동일한 높이)
        title_out.next_to(outward_dots, UP, buff=TITLE_BUFF)
        title_in.next_to(inward_dots, UP, buff=TITLE_BUFF)

        # y좌표 맞추기
        max_y = max(title_out.get_y(), title_in.get_y())
        title_out.set_y(max_y)
        title_in.set_y(max_y)

        # 애니메이션
        self.play(
            Write(title_out),
            Write(title_in)
        )
        self.play(
            Create(outward_dots),
            Create(inward_dots)
        )
        self.wait(2)


class MoveDotToTest(Scene):
    def construct(self):
        # 초기 설정된 점 생성
        dot = PointerLabeledDot(
            label_text="Moving Dot",
            pointer_direction=DR,
            dot_color=BLUE,
            arrow_color=YELLOW,
            label_color=GREEN,
            dot_radius=0.15,
            pointer_length=0.8,
            label_font_size=30
        )
        self.play(Create(dot))
        self.wait(1)

        # 다양한 위치로 이동하며 테스트
        positions = [
            RIGHT * 3,              # 오른쪽
            RIGHT * 3 + UP * 2,     # 우상단
            UP * 2,                 # 위
            LEFT * 3 + UP * 2,      # 좌상단
            LEFT * 3,               # 왼쪽
            LEFT * 3 + DOWN * 2,    # 좌하단
            DOWN * 2,               # 아래
            RIGHT * 3 + DOWN * 2,   # 우하단
            ORIGIN                  # 중앙으로 복귀
        ]

        # 각 위치로 이동
        for pos in positions:
            self.play(
                dot.animate.move_dot_to(pos),
                run_time=0.8
            )
            self.wait(0.3)

        self.play(FadeOut(dot))
        self.wait(1)
