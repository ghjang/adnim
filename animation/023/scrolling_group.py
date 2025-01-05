from enum import Enum, auto
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
    elements: list[VMobject]
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
        self.elements = []

    def _calculate_opacity(self, current_opacity: float | None, position_index: int) -> float:
        if current_opacity is None:
            current_opacity = 1.0 if self.opacity_step < 0 else (
                self.min_opacity or 0.0)

        if self.opacity_step < 0:
            # 음수 스텝: 현재 불투명도에서 감소
            step_for_element = self.opacity_step * \
                (len(self.elements) - position_index - 1)
            future_opacity = max(0.0, current_opacity + step_for_element)
        else:
            # 양수 스텝: 시작 불투명도에서 증가
            step_for_element = self.opacity_step * \
                (len(self.elements) - position_index)
            future_opacity = min(1.0, current_opacity + step_for_element)

        # min_opacity 처리를 음수 스텝일 때만 적용
        if self.min_opacity is not None and self.opacity_step < 0:
            future_opacity = max(future_opacity, self.min_opacity)

        return future_opacity

    def _get_safe_opacity(self, mob: VMobject) -> float:
        """객체의 불투명도를 안전하게 가져오는 헬퍼 메소드"""
        try:
            # 1. get_opacity 메소드 체크
            if hasattr(mob, 'get_opacity'):
                opacity = mob.get_opacity()
                if opacity is not None:
                    return opacity

            # 2. stroke와 fill 불투명도 체크
            opacities = []
            if hasattr(mob, 'get_stroke_opacity'):
                stroke_opacity = mob.get_stroke_opacity()
                if stroke_opacity is not None:
                    opacities.append(stroke_opacity)

            if hasattr(mob, 'get_fill_opacity'):
                fill_opacity = mob.get_fill_opacity()
                if fill_opacity is not None:
                    opacities.append(fill_opacity)

            if opacities:
                return sum(opacities) / len(opacities)

            # 3. opacity 속성 체크
            if hasattr(mob, 'opacity'):
                return float(mob.opacity)

            return 1.0
        except:
            return 1.0

    def _create_scroll_animations(self, spacing: np.ndarray) -> list[Animation]:
        animations: list[Animation] = []

        for i, existing_element in enumerate(self.elements):
            if self.opacity_gradient:
                current_opacity = self._get_safe_opacity(existing_element)
                future_opacity = self._calculate_opacity(current_opacity, i)
                print(f"future_opacity: {future_opacity}")

                animations.append(
                    existing_element
                    .animate.set_opacity(future_opacity).shift(spacing)
                )
            else:
                animations.append(existing_element.animate.shift(spacing))

        if len(self.elements) >= self.max_lines:
            oldest_element: VMobject = self.elements[0]
            animations.append(FadeOut(oldest_element))
            self.elements.pop(0)

        return animations

    def add_element(
        self,
        scene: Scene,
        new_element: VMobject,
        # 레이아웃 관련
        spacing: np.ndarray | None = None,
        spacing_buff: float = 0.35,
        # 애니메이션 타입
        add_animation: AddAnimation = AddAnimation.FADE_IN,
        # 애니메이션 런타임 관련
        scroll_time: float = 0.5,
        creation_time: float = 0.25
    ) -> None:
        new_element.move_to(self.add_position)

        if self.opacity_gradient and self.opacity_step > 0:
            new_element.set_opacity(self.min_opacity or 0.0)

        if spacing is None:
            element_height = new_element.height + spacing_buff
            spacing = self.direction.to_vector() * element_height

        scroll_animations = self._create_scroll_animations(spacing)
        if scroll_animations:
            scene.play(*scroll_animations, run_time=scroll_time)

        self.elements.append(new_element)

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
        # 텍스트 스타일 관련
        font_size: float = 36,
        color: str | None = None,
        is_latex: bool = True,
        # 레이아웃 관련
        spacing: np.ndarray | None = None,
        spacing_buff: float = 0.35,
        # 애니메이션 관련
        animation_type: AddAnimation = AddAnimation.FADE_IN,
        # 기타 옵션
        text_join_char: str = " "
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
            spacing=spacing,
            spacing_buff=spacing_buff,
            add_animation=animation_type
        )
