from manim import *

# 출력 설정
config.frame_width = 10
config.frame_height = 15

# 스타일 상수
ARROW_STYLE = {"color": BLUE_B, "stroke_width": 10, "buff": 0, "tip_length": 0.2}
ARROW_LENGTH = 3.5
ANGLE_ROTATION = 45 * DEGREES
DOT_STYLE = {"color": RED, "radius": 0.1}


class AngleTextToAngleShape(Scene):
    def create_styled_arrow(self, end_point, **kwargs):
        return Arrow(start=ORIGIN, end=end_point, **ARROW_STYLE, **kwargs)

    def construct(self):
        # 텍스트 기본 스타일 설정
        Text.set_default(font_size=120, color=GREEN)

        # 첫 번째 텍스트
        text1 = Text("angle(각도)")
        self.add(text1)
        self.wait(2)

        # 두 번째 텍스트로 변환
        text2 = Text("Angle")
        self.play(ReplacementTransform(text1, text2), run_time=1)

        # 세 번째 텍스트로 변환
        text3 = Text("A", font_size=300)
        self.play(ReplacementTransform(text2, text3), run_time=1)

        # A를 반시계 방향으로 회전
        self.play(Rotate(text3, angle=115 * DEGREES, run_time=1))

        # 넘버플레인 생성 및 페이드인
        plane = NumberPlane(
            x_range=[-8, 8],
            y_range=[-4.5, 4.5],
            background_line_style={"stroke_opacity": 0.5},
        ).set_z_index(-1)

        self.play(FadeIn(plane), text3.animate.set_opacity(0.7), run_time=1)

        # 넘버플레인이 나타난 후에 A를 y축에 맞추고 아래쪽을 원점에 맞춤
        self.play(text3.animate.move_to(ORIGIN, aligned_edge=LEFT + DOWN), run_time=1)

        # Arrow 생성 부분
        a1 = self.create_styled_arrow(RIGHT * ARROW_LENGTH)
        a2 = self.create_styled_arrow(RIGHT * ARROW_LENGTH).rotate(
            angle=ANGLE_ROTATION, about_point=ORIGIN
        )

        # 각도 아크 생성
        angle = Angle(a1, a2, radius=2, color=YELLOW, stroke_width=10, fill_opacity=0.2)

        # 점 생성
        dots = VGroup(
            Dot(ORIGIN, **DOT_STYLE),  # 원점
            Dot(angle.get_start(), **DOT_STYLE),  # 아크 시작점
            Dot(angle.get_end(), **DOT_STYLE),  # 아크 끝점
        )

        # 애니메이션
        self.play(Create(a1), Create(a2), Create(angle), FadeOut(text3), run_time=2)
        self.play(Create(dots), run_time=0.5)

        self.wait(2)
