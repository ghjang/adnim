from typing import override
from manim import *
from scrolling_group import ScrollingGroup, ScrollDirection


class DifferenciationRuleProof(Scene):
    @override
    def construct(self):
        scroller = ScrollingGroup(
            add_position=ORIGIN + DOWN,
            opacity_gradient=True
        )

        constant_multiple_rule = [
            r"\frac{d}{dx}[cf(x)] = cf'(x)",
            r"\text{ where } c \text{ is a constant}",
            r"\text{Proof:}",
            r"\frac{d}{dx}[cf(x)] = \lim_{h \to 0} \frac{cf(x+h) - cf(x)}{h}",
            r"= c \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"= c f'(x)"
        ]

        for rule in constant_multiple_rule:
            scroller.add_text(
                self,
                rule,
            )
            self.wait(0.5)

        self.wait()
