from typing import override
from manim import *
from scrolling_group import ScrollingGroup, ScrollDirection


class ScrollingUpExample(Scene):
    @override
    def construct(self) -> None:
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN,
        )

        texts: list[str] = [
            "First line",
            "Second line",
            "Third line",
            "Fourth line",
            "Fifth line"
        ]

        for text in texts:
            scroller.add_text(self, text)
            self.wait(0.5)

        self.wait()


class ScrollingDownExample(Scene):
    @override
    def construct(self) -> None:
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN,
            direction=ScrollDirection.DOWN
        )

        texts: list[str] = [
            "First line",
            "Second line",
            "Third line",
            "Fourth line",
            "Fifth line"
        ]

        for text in texts:
            scroller.add_text(self, text)
            self.wait(0.5)

        self.wait()


class ScrollingUpGradientExample(Scene):
    @override
    def construct(self) -> None:
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN,
            opacity_gradient=True
        )

        texts: list[str] = [
            "First line",
            "Second line",
            "Third line",
            "Fourth line",
            "Fifth line"
        ]

        for text in texts:
            scroller.add_text(self, text)
            self.wait(0.5)

        self.wait()


class ScrollingDownGradientExample(Scene):
    @override
    def construct(self) -> None:
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN,
            direction=ScrollDirection.DOWN,
            opacity_gradient=True
        )

        texts: list[str] = [
            "First line",
            "Second line",
            "Third line",
            "Fourth line",
            "Fifth line"
        ]

        for text in texts:
            scroller.add_text(self, text)
            self.wait(0.5)

        self.wait()


class ScrollingFadeInGradientExample(Scene):
    @override
    def construct(self) -> None:
        # 양수 스텝으로 설정하여 페이드인 효과
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN,
            opacity_gradient=True,
            opacity_step=0.3,      # 각 스텝마다 30%씩 밝아짐
            min_opacity=0.25        # 10% 불투명도에서 시작
        )

        texts: list[str] = [
            "Fading in",
            "from dark",
            "to bright",
            "step by step",
            "like sunrise"
        ]

        for text in texts:
            scroller.add_text(self, text)
            self.wait(0.5)

        self.wait()


class ScrollingFadeInGradientNoMinExample(Scene):
    @override
    def construct(self) -> None:
        # 완전 투명에서 시작하는 페이드인 효과
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN,
            opacity_gradient=True,
            opacity_step=0.4,      # 각 스텝마다 40%씩 밝아짐
            min_opacity=None       # 완전 투명에서 시작
        )

        texts: list[str] = [
            "Starting from",
            "complete darkness",
            "gradually appearing",
            "into the light",
            "fully visible"
        ]

        for text in texts:
            scroller.add_text(self, text)
            self.wait(0.5)

        self.wait()

# 사용 예시:


class ScrollingCreateExample(Scene):
    @override
    def construct(self) -> None:
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN,
            opacity_gradient=True
        )

        # LaTeX 수식 예시 (가변 인자로 전달)
        scroller.add_text(self, "x^2", "+", "y^2", "=", "r^2")

        # 일반 텍스트 예시 (공백으로 join됨)
        scroller.add_text(self, "This", "is", "joined", "with", "spaces",
                          is_latex=False)

        self.wait()


class GroupOpacityColorTest(Scene):
    @override
    def construct(self) -> None:
        # 기본 그룹 생성
        test_group = VGroup()

        # 다양한 객체들 생성
        text1 = Text("텍스트1", color=RED).set_opacity(0.3)
        text2 = Text("텍스트2", color=BLUE).set_opacity(0.6)
        circle = Circle(radius=0.5, color=GREEN).set_opacity(0.4)
        square = Square(side_length=1, color=YELLOW).set_opacity(0.8)

        # 그룹에 객체들 추가
        test_group.add(text1, text2, circle, square)

        # 객체들을 세로로 정렬
        test_group.arrange(direction=DOWN, buff=0.5)

        # 그룹 전체를 화면에 표시
        self.add(test_group)
        self.wait()

        # 개별 객체의 불투명도 변경 테스트
        # self.play(
        #     text1.animate.set_opacity(1.0),
        #     text2.animate.set_opacity(0.2),
        #     circle.animate.set_opacity(0.9),
        #     square.animate.set_opacity(0.3),
        #     run_time=2
        # )
        self.play(
            text1.animate.set_opacity(1),
            text2.animate.set_opacity(1),
            circle.animate.set_opacity(1),
            square.animate.set_opacity(1),
            run_time=2
        )
        self.wait()

        # 그룹 전체의 색상 변경 테스트
        # NOTE: VGroup의 경우 그룹 전체의 색상을 아래와 같이 변경할 수 있음. 불투명도도 정상적으로 변경됨.
        self.play(
            test_group.animate.set_color(PURPLE).set_opacity(0.2),
            run_time=2
        )
        self.wait()

        # 개별 객체의 색상과 불투명도 동시 변경
        # self.play(
        #     text1.animate.set_color(ORANGE).set_opacity(0.5),
        #     text2.animate.set_color(PINK).set_opacity(1.0),
        #     circle.animate.set_color(BLUE).set_opacity(0.7),
        #     square.animate.set_color(RED).set_opacity(0.8),
        #     run_time=2
        # )
        self.wait()


class ScrollingVGroupTest(Scene):
    @override
    def construct(self) -> None:
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN + DOWN,
            opacity_gradient=True,
            # opacity_step=-0.4,
        )

        # VGroup 1: 텍스트 그룹
        text_group = VGroup()
        text_group.add(
            # Text("제목", color=BLUE, font_size=48),
            # Text("부제목", color=BLUE_B, font_size=32)
            Text("제목", font_size=48),
            Text("부제목", font_size=32)
        ).arrange(DOWN, buff=0.2)

        # VGroup 2: 수식 그룹
        formula_group = VGroup()
        formula_group.add(
            MathTex("F = ma"),
            MathTex("E = mc^2"),
            MathTex("\\sum_{i=1}^{n} i")
        ).arrange(RIGHT, buff=1).set_color(GREEN)

        # VGroup 3: 도형 그룹
        shape_group = VGroup()
        shape_group.add(
            Circle(radius=0.3),
            Square(side_length=0.6),
            Triangle().scale(0.5)
        ).arrange(RIGHT, buff=0.5).set_color(RED)

        # VGroup 4: 혼합 그룹
        mixed_group = VGroup()
        mixed_group.add(
            Text("설명:"),
            Circle(radius=0.2).set_color(YELLOW),
            MathTex("\\rightarrow"),
            Square(side_length=0.4).set_color(PURPLE)
        ).arrange(RIGHT, buff=0.3)

        # 각 VGroup을 ScrollingGroup에 순차적으로 추가
        groups = [text_group, formula_group, shape_group, mixed_group]

        for group in groups:
            scroller.add_element(
                scene=self,
                new_element=group,
                spacing_buff=0.5  # 그룹간 간격 조정
            )
            self.wait(0.5)

        self.wait()


class GreenTextGroupExample(Scene):
    @override
    def construct(self) -> None:
        scroller: ScrollingGroup = ScrollingGroup(
            add_position=ORIGIN + DOWN * 2,
            opacity_gradient=True,
            max_lines=4,
            opacity_step=-0.3  # 페이드 아웃 효과
        )

        # 여러 줄의 녹색 텍스트 그룹들 정의
        group1 = VGroup(
            Text("System Status", font_size=48),
            # Text("● ONLINE", font_size=36),
            # Text("● ACTIVE", font_size=36)
        ).arrange(DOWN, buff=0.2).set_color(GREEN)

        group2 = VGroup(
            Text("Memory Usage", font_size=48),
            # Text("RAM: 42%", font_size=36),
            # Text("CPU: 28%", font_size=36)
        ).arrange(DOWN, buff=0.2).set_color(GREEN)

        group3 = VGroup(
            Text("Network Status", font_size=48),
            # Text("↑ 25MB/s", font_size=36),
            # Text("↓ 42MB/s", font_size=36)
        ).arrange(DOWN, buff=0.2).set_color(GREEN)

        group4 = VGroup(
            Text("Test Status", font_size=48),
            # Text("↑ 25MB/s", font_size=36),
            # Text("↓ 42MB/s", font_size=36)
        ).arrange(DOWN, buff=0.2).set_color(GREEN)

        group5 = VGroup(
            Text("Test1 Status", font_size=48),
            # Text("↑ 25MB/s", font_size=36),
            # Text("↓ 42MB/s", font_size=36)
        ).arrange(DOWN, buff=0.2).set_color(GREEN)

        group4_copy = group4.copy().set_opacity(0.7)
        group5_copy = group5.copy().set_opacity(1)
        self.add(VGroup(group4_copy, group5_copy).arrange(DOWN, buff=0.2).to_edge(UL))

        # 각 그룹을 순차적으로 추가
        for group in [group1, group2, group3, group4, group5]:
            scroller.add_element(
                scene=self,
                new_element=group,
            )
            self.wait(0.5)

        self.wait()
