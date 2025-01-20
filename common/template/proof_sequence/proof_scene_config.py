from dataclasses import dataclass, field
from typing import List
from manim import *


@dataclass
class ProofSceneConfig:
    # 공통 설정
    font_size: int = 60
    formula_color: ManimColor = field(default_factory=lambda: GREEN)
    v_spacing_buff: float = 0.25
    h_buff: float = 0.2
    animation_pause: float = 0.5

    # 타이틀 설정
    title_font_size: int = 64
    title_position: np.ndarray = field(default_factory=lambda: UP * 2)
    title_colors: List[str] = field(
        default_factory=lambda: ["#FFD700", "#50C878", "#4B0082", "#800080"]
    )
    title_glow_primary: dict = field(
        default_factory=lambda: {
            "color": "#FFD700",
            "width": 8,
            "opacity": 0.15
        }
    )
    title_glow_secondary: dict = field(
        default_factory=lambda: {
            "color": "#50C878",
            "width": 4,
            "opacity": 0.1
        }
    )
    title_intro_formula_size: int = 72
    title_display_time: float = 2.0
    title_vertical_offset: np.ndarray = field(
        default_factory=lambda: DOWN * 0.5
    )
    skip_intro_title: bool = False

    # 결론 설정
    conclusion_color: ManimColor = field(default_factory=lambda: PINK)
    qed_font_size: int = 36
    qed_buff: float = 0.2
    qed_shift: np.ndarray = field(
        default_factory=lambda: UP * 0.25
    )
    conclusion_animation_time: float = 1.0

    # 레이아웃 설정
    start_position: np.ndarray = field(
        default_factory=lambda: ORIGIN + DOWN * 1.5
    )
    scene_end_pause: float = 2.0
