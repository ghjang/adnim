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
