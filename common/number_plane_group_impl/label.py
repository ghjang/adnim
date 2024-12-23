from manim import *

from .number_plane_group_base import (
    MobjectType,
    NumberPlaneGroupBase
)


class LabelMixIn(NumberPlaneGroupBase):
    def __init__(self, **kwargs):
        if not hasattr(self, '_init_called'):
            super().__init__(**kwargs)
        self._ensure_single_init()

    def add_label(self,
                  text,
                  position=None,  # (x,y) 좌표
                  name=None,
                  color=WHITE,
                  font_size=36,
                  tex_template=None,  # LaTeX 템플릿 설정 가능
                  direction=RIGHT,    # 기본 방향
                  buff=0.1):          # 기본 간격
        """임의의 위치에 라벨 추가"""
        if name is None:
            name = f"label_{len([m for m in self.submobjects if m.metadata.get('type') == MobjectType.LABEL])}"

        # LaTeX 수식 여부에 따라 적절한 객체 생성
        if tex_template:
            label = MathTex(
                text,
                color=color,
                font_size=font_size,
                tex_template=tex_template
            )
        else:
            label = Text(
                text,
                color=color,
                font_size=font_size
            )

        if position:
            # 좌표계의 위치로 변환
            point = self.plane.c2p(*position)

            # 위치 지정
            label.next_to(point, direction, buff=buff)

        self._ensure_metadata(label)
        label.metadata = {"type": MobjectType.LABEL, "name": name}

        self.add(label)
        return label

    def add_tex_label(self,
                      text,
                      position=None,
                      name=None,
                      color=WHITE,
                      font_size=36,
                      direction=RIGHT,
                      buff=0.1):
        return self.add_label(
            text,
            position,
            name=name,
            color=color,
            font_size=font_size,
            tex_template=TexTemplate(),
            direction=direction,
            buff=buff
        )

    def remove_label(self, name):
        """라벨 제거"""
        label = self.find_mobject(name, MobjectType.LABEL)
        if (label):
            self.remove(label)

    def get_label(self, name):
        """특정 라벨 가져오기"""
        return self.find_mobject(name, MobjectType.LABEL)

    def add_brace(self,
                  mobject,
                  direction=DOWN,
                  name=None,
                  buff=0.1,
                  color=WHITE,
                  text=None,
                  text_color=None,
                  text_buff=0.1,
                  font_size=36):  # 텍스트 색상을 독립적으로 설정
        """Brace(중괄호) 추가 메서드

        Args:
            mobject: 브레이스를 추가할 객체
            direction: 브레이스의 방향 (DOWN, UP, LEFT, RIGHT)
            name: 브레이스의 이름 (None이면 자동생성)
            buff: 브레이스와 객체 사이의 간격
            color: 브레이스의 색상
            text: 브레이스에 표시할 텍스트 (선택사항)
            font_size: 텍스트의 크기
            text_color: 텍스트의 색상 (None이면 브레이스와 같은 색상)

        Returns:
            tuple: (Brace, MathTex or None) - 브레이스와 텍스트 객체 튜플
        """
        if name is None:
            name = f"brace_{len(list(self.iter_mobjects(obj_type='BRACE')))}"

        # Brace 객체 생성
        brace = Brace(
            mobject,
            direction=direction,
            buff=buff,
            color=color
        )

        # 메타데이터 설정
        self._ensure_metadata(brace)
        brace.metadata = {
            "type": "BRACE",
            "name": name,
            "direction": direction,
            "has_text": text is not None
        }

        self.add(brace)

        # 텍스트 생성 및 추가
        tex = None
        if (text):
            if (text_color is None):
                text_color = color

            tex = brace.get_tex(text, buff=text_buff)
            tex.set_font_size(font_size)
            tex.set_color(text_color)

            # 텍스트 메타데이터 설정
            self._ensure_metadata(tex)
            tex.metadata = {
                "type": "BRACE_TEXT",
                "name": f"{name}_text",
                "parent_brace": name
            }

            # 텍스트 객체 따로 추가
            self.add(tex)

        return (brace, tex)
