from pathlib import Path
from manim import *
from .web import WebImageMobject

import requests


# OpenMoji 프로젝트의 기본 URL과 이미지 크기 상수
OPENMOJI_BASE_URL = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/master"
OPENMOJI_COLOR_SIZE = "618x618"


class OpenMojiMixin:
    """OpenMoji 이모지 처리를 위한 공통 기능을 제공하는 Mixin 클래스"""

    @staticmethod
    def _convert_emoji_to_hex_codes(emoji: str) -> str:
        """이모지를 하이픈으로 구분된 16진수 코드 시퀀스로 변환"""
        return '-'.join(f'{ord(c):x}' for c in emoji)


class EmojiImageMobject(WebImageMobject, OpenMojiMixin):
    """이모지를 Manim 애니메이션에서 사용할 수 있는 이미지 객체로 변환"""

    def __init__(self, emoji: str | int, **kwargs):
        if isinstance(emoji, int):
            img_url = self._get_emoji_url_from_hex(emoji)
        else:
            img_url = self._get_emoji_url(emoji)
            
        WebImageMobject.__init__(self, img_url, **kwargs)

    @classmethod
    def _get_emoji_url(cls, emoji: str) -> str:
        """이모지 문자에 해당하는 PNG URL 반환"""
        emoji_code = cls._convert_emoji_to_hex_codes(emoji).upper()
        return f'{OPENMOJI_BASE_URL}/color/{OPENMOJI_COLOR_SIZE}/{emoji_code}.png'

    @classmethod
    def _get_emoji_url_from_hex(cls, hex_code: str | int) -> str:
        """16진수 코드에 해당하는 PNG URL 반환"""
        if isinstance(hex_code, int):
            hex_code = f"{hex_code:x}"
        hex_code = str(hex_code).upper()
        return f'{OPENMOJI_BASE_URL}/color/{OPENMOJI_COLOR_SIZE}/{hex_code}.png'


class EmojiSVGMobject(SVGMobject, OpenMojiMixin):
    """이모지를 Manim 애니메이션에서 사용할 수 있는 SVG 객체로 변환"""

    def __init__(self, emoji, **kwargs):
        try:
            # 임시 파일 생성
            path_svg = Path.cwd() / f'{self._convert_emoji_to_hex_codes(emoji).upper()}.svg'
            # requests 사용하여 다운로드
            url = f'{OPENMOJI_BASE_URL}/color/svg/{path_svg.stem}.svg'
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                path_svg.write_bytes(response.content)
            
            SVGMobject.__init__(self, str(path_svg), **kwargs)
        finally:
            if path_svg.exists():
                path_svg.unlink()
