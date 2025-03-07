from manim import *


class GetEntriesExample(Scene):
    def construct(self):
        table = Table(
            [["First", "Second"], ["Third", "Fourth"]], element_to_mobject=Text
        )
        ent = table.get_entries()
        for item in ent:
            item.set_color(random_bright_color())
        table.get_entries((2, 2)).rotate(PI)
        table.get_entries((1, 1)).become(
            Text("Hello").move_to(table.get_entries((1, 1)))
        )
        self.add(table)
