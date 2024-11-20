from manim import *


class SceneSectionTest(Scene):
    def construct(self):
        self.next_section("Section 1")

        # some animations

        self.next_section("Section 2", skip_animations=True)

        # some animations

        self.next_section("Section 3")

        # some animations


class SceneSectionTest2(Scene):
    def construct(self):
        self.next_section("Section 1")

        # some animations

        self.next_section("Section 2")

        # some animations
