from manim import *
from common.web import WebImageMobject
from common.open_emoji import EmojiImageMobject


class WebImageTest(Scene):
    def construct(self):
        web_img = WebImageMobject(
            'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
        )
        self.add(web_img)


class WebImageTest1(Scene):
    def construct(self):
        keyword = '청설'
        search_url = f'https://search.naver.com/search.naver?ssc=tab.image.all&where=image&sm=tab_jum&query={keyword}'

        web_imgs = WebImageMobject.from_page(
            search_url,
            fetch_limit=12,
            selector='span[class=thumb]'
        )

        if web_imgs:
            image_grid = Group(*web_imgs).arrange_in_grid(
                rows=3,
                cols=4,
                buff=0.2
            )

            image_grid.set_width(config.frame_width - 0.5)
            if image_grid.height > config.frame_height - 0.5:
                image_grid.set_height(config.frame_height - 0.5)

            self.add(image_grid)


class EmojiImageTest(Scene):
    def construct(self):
        emoji_img = EmojiImageMobject('🐶')
        self.add(emoji_img)


class EmojiImageTest1(Scene):
    def construct(self):
        self.camera.background_color = BLUE_A
        face_emojis = [
            '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇',
            '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚',
        ]
        emoji_imgs = [EmojiImageMobject(emoji).scale(0.4) for emoji in face_emojis]
        group = Group(*emoji_imgs).arrange_in_grid(rows=4, cols=5, buff=0.2)
        self.add(group)
