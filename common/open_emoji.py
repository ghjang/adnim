import numpy as np
import requests
import urllib.request
from pathlib import Path
from PIL import Image
from manim import *

# OpenMoji 프로젝트의 기본 URL과 이미지 크기 상수
OPENMOJI_BASE_URL = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/master"
OPENMOJI_COLOR_SIZE = "618x618"


def convert_emoji_to_hex_codes(emoji: str) -> str:
    """이모지를 하이픈으로 구분된 16진수 코드 시퀀스로 변환합니다.

    Args:
        emoji: 변환할 이모지 문자열

    Returns:
        하이픈으로 구분된 16진수 코드들

    Example:
        >>> convert_emoji_to_hex_codes("👋")
        "1f44b"
        >>> convert_emoji_to_hex_codes("👨‍👩‍👦")
        "1f468-200d-1f469-200d-1f466"
    """
    return '-'.join(f'{ord(c):x}' for c in emoji)


def get_open_emoji_image(emoji: str) -> Image:
    """OpenMoji 프로젝트에서 이모지의 PNG 이미지를 가져옵니다.

    Args:
        emoji: 다운로드할 이모지 문자

    Returns:
        PIL Image 객체
    """
    emoji_code = convert_emoji_to_hex_codes(emoji)
    emoji_code = emoji_code.upper()  # needed for openmojis
    url = f'{OPENMOJI_BASE_URL}/color/{OPENMOJI_COLOR_SIZE}/{emoji_code}.png'
    im = Image.open(requests.get(url, stream=True).raw)
    return im


def get_open_emoji_image_from_hex(hex_code: str | int) -> Image:
    """16진수 코드를 사용하여 OpenMoji 프로젝트에서 이모지 PNG 이미지를 가져옵니다.

    Args:
        hex_code: 이모지의 16진수 코드 (문자열 또는 정수)

    Returns:
        PIL Image 객체
    """
    if isinstance(hex_code, int):
        hex_code = f"{hex_code:x}"
    hex_code = str(hex_code).upper()
    url = f'{OPENMOJI_BASE_URL}/color/{OPENMOJI_COLOR_SIZE}/{hex_code}.png'
    im = Image.open(requests.get(url, stream=True).raw)
    return im


def get_open_emoji_svg(emoji: str, download_path: Path = None) -> Path:
    """OpenMoji 프로젝트에서 이모지의 SVG 파일을 다운로드합니다.

    Args:
        emoji: 다운로드할 이모지 문자
        download_path: SVG 파일을 저장할 경로 (기본값: 현재 작업 디렉토리)

    Returns:
        다운로드된 SVG 파일의 경로
    """
    emoji_code = convert_emoji_to_hex_codes(emoji)
    emoji_code = emoji_code.upper()  # needed for openmojis
    url = f'{OPENMOJI_BASE_URL}/color/svg/{emoji_code}.svg'
    if download_path is None:
        download_path = Path.cwd() / f'{emoji_code}.svg'
    urllib.request.urlretrieve(url, download_path)
    return download_path


class EmojiImageMobject(ImageMobject):
    """이모지를 Manim 애니메이션에서 사용할 수 있는 이미지 객체로 변환합니다.

    PNG 형식의 이모지 이미지를 사용하며, 투명도를 지원합니다.
    """

    def __init__(self, emoji: str | int, **kwargs):
        if isinstance(emoji, int):
            im = get_open_emoji_image_from_hex(emoji)
        else:
            im = get_open_emoji_image(emoji)
        emoji_img = np.array(im.convert('RGBA'))
        ImageMobject.__init__(self, emoji_img, **kwargs)


class EmojiSVGMobject(SVGMobject):
    """이모지를 Manim 애니메이션에서 사용할 수 있는 SVG 객체로 변환합니다.

    SVG 형식을 사용하여 더 나은 벡터 그래픽 품질을 제공합니다.
    다운로드된 SVG 파일은 사용 후 자동으로 삭제됩니다.
    """

    def __init__(self, emoji, **kwargs):
        path_svg = get_open_emoji_svg(emoji)
        SVGMobject.__init__(self, str(path_svg), **kwargs)
        path_svg.unlink()  # delete downloaded svg again locally
