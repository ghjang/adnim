from manim import *


class TextMoveTest(Scene):
    def construct(self):
        # 기본 텍스트
        text1 = Text("Text A", color=BLUE)
        self.play(Write(text1))
        self.wait(1)

        # 이동 테스트
        text2 = Text("Text B", color=RED).shift(RIGHT * 3)
        self.play(
            Transform(text1, text2),
            run_time=1
        )
        self.wait(1)

        # ReplacementTransform 테스트
        text3 = Text("Text C", color=GREEN).shift(UP * 2)
        self.play(
            ReplacementTransform(text1, text3),
            run_time=1
        )
        self.wait(1)

        # FadeTransform 테스트
        text4 = Text("Text D", color=YELLOW).shift(LEFT * 3)
        self.play(
            FadeTransform(text3, text4),
            run_time=1
        )
        self.wait(1)

        self.play(FadeOut(text4))
        self.wait(1)


class TextGroupMoveTest(Scene):
    def construct(self):
        # 텍스트와 점을 포함하는 그룹 생성
        def create_text_group(text, pos=ORIGIN, color=WHITE):
            group = VGroup()
            dot = Dot(point=pos, color=color)
            text = Text(text, color=color).next_to(dot, RIGHT)
            group.add(dot, text)
            return group

        # 초기 그룹
        group1 = create_text_group("Group A", ORIGIN, BLUE)
        self.play(Create(group1))
        self.wait(1)

        # Transform 테스트
        group2 = create_text_group("Group B", RIGHT*3, RED)
        self.play(
            Transform(group1, group2),
            run_time=1
        )
        self.wait(1)

        # ReplacementTransform 테스트
        group3 = create_text_group("Group C", UP*2, GREEN)
        self.play(
            ReplacementTransform(group1, group3),
            run_time=1
        )
        self.wait(1)

        # 개별 요소 변환 테스트
        group4 = create_text_group("Group D", LEFT*3, YELLOW)
        self.play(
            Transform(group3[0], group4[0]),  # 점 변환
            Transform(group3[1], group4[1]),  # 텍스트 변환
            run_time=1
        )
        self.wait(1)

        self.play(FadeOut(group3))
        self.wait(1)


class TextGroupTransformTest(Scene):
    def construct(self):
        # 복합 그룹 생성 함수
        def create_complex_group(text, pos=ORIGIN, color=WHITE):
            group = VGroup()
            dot = Dot(point=pos, color=color)
            arrow = Arrow(
                start=pos + LEFT,
                end=pos,
                color=color,
                buff=0.1
            )
            text = Text(text, color=color).next_to(arrow.get_start(), LEFT)
            group.add(dot, arrow, text)
            return group

        # 초기 그룹 생성
        group1 = create_complex_group("Start", ORIGIN, BLUE)
        self.play(Create(group1))
        self.wait(1)

        # 전체 그룹 Transform 테스트
        positions = [RIGHT*3, UP*2, LEFT*3, DOWN*2, ORIGIN]
        colors = [RED, GREEN, YELLOW, PURPLE, BLUE]
        texts = ["Right", "Up", "Left", "Down", "End"]

        for pos, color, text in zip(positions, colors, texts):
            new_group = create_complex_group(text, pos, color)
            self.play(
                Transform(group1, new_group),
                run_time=1
            )
            self.wait(0.5)

        self.play(FadeOut(group1))
        self.wait(1)
