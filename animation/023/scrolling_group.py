from enum import Enum, auto
from numpy import ndarray
from manim import *


class ScrollDirection(Enum):
    UP = "up"
    DOWN = "down"

    def to_vector(self) -> np.ndarray:
        return {
            ScrollDirection.UP: UP,
            ScrollDirection.DOWN: DOWN
        }[self]


class AddAnimation(Enum):
    FADE_IN = auto()    # 기본값: 페이드인
    CREATE = auto()     # manim의 Create 애니메이션
    NONE = auto()       # 애니메이션 없이 바로 추가


class ScrollingGroup(VGroup):
    max_lines: int
    add_position: np.ndarray
    direction: ScrollDirection
    opacity_gradient: bool
    opacity_step: float
    min_opacity: float | None

    def __init__(
        self,
        max_lines: int = 3,
        add_position: np.ndarray = ORIGIN,
        direction: ScrollDirection = ScrollDirection.UP,
        opacity_gradient: bool = False,
        opacity_step: float = -0.25,
        min_opacity: float | None = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.max_lines = max_lines
        self.add_position = add_position
        self.direction = direction
        self.opacity_gradient = opacity_gradient
        self.opacity_step = opacity_step
        self.min_opacity = min_opacity

    def _calculate_element_next_opacity(
        self,
        elem_curr_index: int
    ) -> float:
        scroll_window_size = self.max_lines

        curr_added_elem_cnt = len(self.submobjects)
        elem_next_index = elem_curr_index

        if curr_added_elem_cnt >= scroll_window_size:
            elem_next_index = elem_curr_index - 1

        # NOTE:
        # '음수 스텝'의 경우 새로 추가되는 항목이 가장 밝게 표시되고,
        # 기존에 먼저 추가된 항목들이 더 흐리게 표시되어야 함.
        #
        # '양수 스텝'의 경우 새로 추가되는 항목이 가장 흐리게 표시되고,
        # 기존에 먼저 추가된 항목들이 더 밝게 표시되어야 함.
        step_factor = curr_added_elem_cnt - elem_next_index
        if self.opacity_step < 0:
            base_opacity = 1.0
        else:
            if curr_added_elem_cnt < scroll_window_size:
                step_factor += 1
            base_opacity = self.min_opacity or 0.0
        future_opacity = base_opacity + (self.opacity_step * step_factor)

        # min_opacity 처리를 음수 스텝일 때만 적용
        if self.min_opacity is not None and self.opacity_step < 0:
            future_opacity = max(future_opacity, self.min_opacity)

        return future_opacity

    def _create_scroll_animations(
        self,
        shift_delta: np.ndarray
    ) -> list[Animation]:
        animations: list[Animation] = []

        for i, existing_element in enumerate(self.submobjects):
            if self.opacity_gradient:
                elem_opacity = self._calculate_element_next_opacity(i)

                animations.append(
                    existing_element
                    .animate.shift(shift_delta).set_opacity(elem_opacity)
                )
            else:
                animations.append(existing_element.animate.shift(shift_delta))

        if len(self.submobjects) >= self.max_lines:
            oldest_element: VMobject = self.submobjects[0]
            animations.append(FadeOut(oldest_element))
            self.remove(oldest_element)

        return animations

    def add_element(
        self,
        scene: Scene,
        new_element: VMobject,
        v_spacing: np.ndarray | None = None,
        v_spacing_buff: float = 0.35,
        h_offset: float = 0.0,            # 수평 위치 조정값
        h_align: ndarray | None = None,   # 수평 정렬 방향 (LEFT/RIGHT/None)
        h_align_buff: float = 0.0,        # 수평 정렬시 여백
        add_animation: AddAnimation = AddAnimation.FADE_IN,
        scroll_time: float = 0.5,
        creation_time: float = 0.25
    ) -> None:
        # NOTE:
        # 신규로 추가된 항목이 가장 흐리게 표시되고,
        # 기존에 먼저 추가된 항목들이 더 밝아지도록 'self.opacity_step'이 '양수'로 설정된 경우
        if self.opacity_gradient and self.opacity_step > 0:
            new_element.set_opacity(self.min_opacity or 0.0)

        # 신규로 추가된 항목의 '높이' 정보(spacing)가 명시되지 않은 경우
        if v_spacing is None:
            element_height = new_element.height + v_spacing_buff
            v_spacing = self.direction.to_vector() * element_height

        scroll_animations = self._create_scroll_animations(
            shift_delta=v_spacing
        )
        if scroll_animations:
            scene.play(*scroll_animations, run_time=scroll_time)

        self.add(new_element)

        # 기본 위치 설정 (수평 오프셋 적용)
        base_position = self.add_position + RIGHT * h_offset
        new_element.move_to(base_position)

        # 수평 정렬이 지정된 경우 to_edge 적용
        if h_align is not None:
            new_element.to_edge(h_align, buff=h_align_buff)

        match add_animation:
            case AddAnimation.FADE_IN:
                scene.play(FadeIn(new_element), run_time=creation_time)
            case AddAnimation.CREATE:
                scene.play(Create(new_element), run_time=creation_time)
            case AddAnimation.NONE:
                scene.add(new_element)

    def add_text(
        self,
        scene: Scene,
        *text: str,
        text_join_char: str = " ",
        font_size: float = 36,
        color: str | None = None,
        is_latex: bool = True,
        v_spacing: np.ndarray | None = None,
        v_spacing_buff: float = 0.35,
        h_offset: float = 0.0,
        h_align: ndarray | None = None,
        h_align_buff: float = 0.0,
        animation_type: AddAnimation = AddAnimation.FADE_IN
    ) -> None:
        if is_latex:
            latex_obj: MathTex = MathTex(*text, font_size=font_size)
            if color is not None:
                latex_obj.set_color(color)
            text_obj = latex_obj
        else:
            text_obj: Text = Text(
                text_join_char.join(text),
                font_size=font_size,
                color=color if color is not None else WHITE
            )

        self.add_element(
            scene=scene,
            new_element=text_obj,
            v_spacing=v_spacing,
            v_spacing_buff=v_spacing_buff,
            h_offset=h_offset,
            h_align=h_align,
            h_align_buff=h_align_buff,
            add_animation=animation_type
        )
