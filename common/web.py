from __future__ import annotations

from typing import List
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from manim import *

import numpy as np
import requests


class WebImageMobject(ImageMobject):
    def __init__(self, img_src: str | Image.Image, **kwargs):
        if isinstance(img_src, str):
            img = self._get_web_image(img_src)
        else:
            img = img_src

        with img:
            im = np.array(img.convert('RGBA'))
            ImageMobject.__init__(self, im, **kwargs)

    @staticmethod
    def _get_web_image(img_url: str) -> Image:
        """웹에서 이미지를 가져온다.

        Args:
            img_url: 이미지 URL

        Returns:
            PIL Image 객체
        """
        with requests.get(img_url, stream=True) as response:
            response.raise_for_status()
            with Image.open(response.raw) as im:
                return im.copy()

    @classmethod
    def from_page(
        cls,
        page_url: str,
        fetch_limit: int = 10,
        selector: str | None = None
    ) -> List[WebImageMobject]:
        """웹페이지에서 이미지들을 가져와 WebImageMobject 리스트로 반환한다."""
        images = []

        with requests.get(page_url) as response:
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            img_tags = []
            if selector:
                elements = soup.select(selector)
                for element in elements:
                    img_tags.extend(element.find_all('img'))
            else:
                img_tags = soup.find_all('img')

            for img in img_tags:
                img_url = img.get('src')
                if not img_url:
                    continue

                img_url = urljoin(page_url, img_url)
                try:
                    web_img = cls._get_web_image(img_url)
                    images.append(cls(web_img))
                    if len(images) >= fetch_limit:
                        break
                except (requests.RequestException, IOError) as e:
                    print(f"Error fetching image {img_url}: {e}")
                    continue

        return images
