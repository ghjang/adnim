
from manim import *
from typing import List, Tuple, Any, Optional

class TexBuilder:
    """Tex 객체 생성을 위한 유틸리티 클래스

    수식과 색상 정보를 튜플 리스트로 받아 색상이 적용된 Tex 객체를 생성합니다.
    """

    def __init__(self, font_size: int = 24):
        self.font_size = font_size

    def extract_items(self, parts: List[Tuple], idx: int) -> List:
        """튜플 리스트에서 특정 인덱스의 아이템만 추출

        Args:
            parts: 추출할 데이터가 있는 튜플 리스트
            idx: 추출할 튜플의 인덱스

        Returns:
            List: 추출된 아이템들의 리스트
        """
        return [part[idx] for part in parts]

    def create_colored_tex(
        self,
        eq_parts: List[Tuple[str, Any]],
        position: Optional[Tuple] = None,
        default_color: Any = WHITE,
        **kwargs
    ) -> MathTex:
        """색상이 적용된 MathTex 객체 생성

        Args:
            eq_parts: [(수식, 색상), ...] 또는 [수식, ...] 형태의 리스트
            position: (참조객체, 방향, 간격) 형태의 위치 정보 튜플
            default_color: 기본 텍스트 색상
            **kwargs: MathTex 생성시 추가 인자

        Returns:
            MathTex: 색상이 적용된 수식 객체

        Example:
            >>> eq_parts = [(r"f'(x)", BLUE), ("=", WHITE), ("2x", RED)]
            >>> tex = builder.create_colored_tex(eq_parts)
        """
        # 문자열만 지정된 경우 기본 색상으로 처리
        eq_parts = [(part, default_color) if isinstance(
            part, str) else part for part in eq_parts]
        formulas = self.extract_items(eq_parts, 0)

        tex = MathTex(
            *formulas,
            **kwargs
        )

        for i, (_, color) in enumerate(eq_parts):
            tex[i].set_color(color)

        if position:
            ref_obj, direction, buff = position
            tex.next_to(ref_obj, direction, buff=buff)

        return tex

    def create_equation_table(
        self,
        contents: List[Tuple[Any, Optional[str]]],
        default_color: Any = WHITE,
        description_color: Any = WHITE,
        dummy_text: str = "DUMMY-Qj",
        dummy_opacity: float = 0,
        element_buff: float = 0.3,
        v_buff: float = 0.8,
        h_buff: float = 2.0,
        **kwargs
    ) -> MobjectTable:
        """수식과 설명을 포함한 테이블 생성

        Args:
            contents: [(수식 또는 [(수식, 색상)], 설명), ...] 형태의 리스트
            default_color: 기본 텍스트 색상
            description_color: 설명 텍스트 색상
            dummy_text: 더미 텍스트
            dummy_opacity: 더미 텍스트의 투명도
            element_buff: 수식과 설명 사이의 간격
            v_buff: 테이블의 세로 간격
            h_buff: 테이블의 가로 간격
            **kwargs: MobjectTable 생성시 추가 인자

        Returns:
            MobjectTable: 수식과 설명이 포함된 테이블 객체
        """
        equations = []
        descriptions = []

        for eq_parts, desc in contents:
            # 문자열만 지정된 경우 기본 색상으로 처리
            if isinstance(eq_parts, str):
                eq_parts = [(eq_parts, default_color)]
            else:
                eq_parts = [(part, default_color) if isinstance(
                    part, str) else part for part in eq_parts]
            equation = self.create_colored_tex(eq_parts)
            if desc:
                equations.append(equation)
                description = Text(
                    "; " + desc, font_size=self.font_size, color=description_color)
                descriptions.append(description)
            else:
                if equations:
                    last_eq = equations[-1]
                    if isinstance(last_eq, VGroup):
                        last_eq.add(equation)
                        last_eq.arrange(DOWN, buff=element_buff)
                    else:
                        last_eq = VGroup(
                            last_eq, equation).arrange(DOWN, buff=element_buff)
                        equations[-1] = last_eq

                    dummy_desc = Text(
                        dummy_text, font_size=self.font_size, fill_opacity=dummy_opacity)
                    last_desc = descriptions[-1]
                    if isinstance(last_desc, VGroup):
                        last_desc.add(dummy_desc)
                        last_desc.arrange(DOWN, buff=element_buff)
                    else:
                        last_desc = VGroup(
                            last_desc, dummy_desc).arrange(DOWN, buff=element_buff)
                        descriptions[-1] = last_desc
                else:
                    equations.append(equation)

        table = MobjectTable(
            [[eq, desc] for eq, desc in zip(equations, descriptions)],
            include_outer_lines=False,
            include_background_rectangle=False,
            line_config={"stroke_opacity": 0},  # 선을 완전히 투명하게 설정
            v_buff=v_buff,
            h_buff=h_buff,
            arrange_in_grid_config={"cell_alignment": LEFT},
            **kwargs
        )

        return table