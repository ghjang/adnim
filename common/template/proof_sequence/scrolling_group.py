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
        elem_curr_index: int,
        new_elem_index: int
    ) -> float:
        # 새로운 요소와의 거리 계산
        distance = new_elem_index - elem_curr_index

        if self.opacity_step < 0:
            # 음수 스텝:
            # 새로운 요소가 가장 밝음.
            # 거리가 멀수록 더 어두워짐.
            base_opacity = 1.0
        else:
            # 양수 스텝:
            # 새로운 요소가 가장 어두움.
            # 거리가 멀수록 더 밝아짐 (스텝을 바로 거리에 곱함).
            base_opacity = self.min_opacity or 0.0

        future_opacity = base_opacity + (self.opacity_step * distance)

        # min_opacity 처리 (음수 스텝일 때만)
        if self.min_opacity is not None and self.opacity_step < 0:
            future_opacity = max(future_opacity, self.min_opacity)

        # 최종 불투명도는 0.0과 1.0 사이로 제한
        return max(0.0, min(1.0, future_opacity))

    def _create_scroll_animations(
        self,
        v_spacing: np.ndarray | None = None,
        v_spacing_buff: float = 0.35,
        new_element: VMobject | None = None
    ) -> list[Animation]:
        animations: list[Animation] = []
        shift_direction = self.direction.to_vector()

        # 신규 요소의 인덱스 계산
        new_elem_index = len(self.submobjects)

        # 모든 기존 요소들을 동일하게 이동
        if v_spacing is None and new_element is not None:
            shift_delta = shift_direction * \
                (new_element.height + v_spacing_buff)
        else:
            # 고정 간격이 지정된 경우
            shift_delta = shift_direction * (v_spacing + v_spacing_buff)

        # 모든 기존 요소에 동일한 이동값 적용
        for i, existing_element in enumerate(self.submobjects):
            if self.opacity_gradient:
                elem_opacity = self._calculate_element_next_opacity(
                    i, new_elem_index)
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

        # 신규 요소를 전달하여 스크롤 애니메이션 생성
        scroll_animations = self._create_scroll_animations(
            v_spacing=v_spacing,
            v_spacing_buff=v_spacing_buff,
            new_element=new_element
        )

        if scroll_animations:
            scene.play(*scroll_animations, run_time=scroll_time)

        self.add(new_element)

        # 기본 위치 설정 (수평/수직 오프셋 적용)
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
