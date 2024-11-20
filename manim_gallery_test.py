from manim import *
from common.open_emoji import *


class EmojiExample1(Scene):
    def construct(self):
        self.camera.background_color = YELLOW_A
        em = EmojiImageMobject('👨‍👩‍👦').scale(1.1)
        # when using OpenEmoji, please give credits e.g. like this:
        # 'All emojis designed by OpenMoji – the open-source emoji and icon project. License: CC BY-SA 4.0'
        t = Text('OpenMoji').scale(2.5)
        Group(em, t).arrange(DOWN).scale(1.5)
        self.add(em, t)


class EmojiExample2(Scene):
    def construct(self):
        self.camera.background_color = BLUE_A
        face_emojis = [
            0x1F642, 0x1F600, 0x1F603,
            0x1F604, 0x1F601, 0x1F606,
            0x1F605, 0x1F923, 0x1F602
        ]
        emojis = [EmojiImageMobject(e).scale(0.5) for e in face_emojis]
        group = Group(*emojis).arrange_in_grid(3, 3, buff=0.5)
        self.add(group)

        self.wait(2)
        self.play(FadeOut(group))

        group.remove(*emojis)
        for emoji in emojis:
            emoji.move_to(ORIGIN).scale(3)

        for i in range(1, len(emojis)):
            self.play(
                ReplacementTransform(emojis[i-1], emojis[i])
            )
            self.wait(0.25)


class EmojiSVGExample1(Scene):
    def construct(self):
        self.camera.background_color = GREEN_A
        em = EmojiSVGMobject('🐶').scale(2.5)
        t = Text('OpenMoji (SVG)').scale(2)
        Group(em, t).arrange(DOWN).scale(1.4)
        self.add(em, t)
