from manim import *


class LogicGateStyle:
    """논리 게이트들의 공통 스타일 정의"""
    DEFAULT_COLOR = BLUE
    DEFAULT_SIZE = 1
    DEFAULT_CIRCLE_RATIO = 0.05
    DEFAULT_STROKE_WIDTH = 1.5
    DEFAULT_FILL_OPACITY = 0.8
    DEFAULT_STROKE_LIGHTEN = 0.3

    # 입출력 포인트 관련 설정
    PORT_VERTICAL_SPACING = 0.25  # 다중 입력 포트간 세로 간격 비율
    PORT_RADIUS = 0.02           # 포트 크기 조정 (기존보다 약간 작게)
    PORT_OPACITY = 0.3           # 포트 투명도 증가 (덜 눈에 띄게)
    PORT_STYLE = {
        "stroke_width": 1,
        "stroke_opacity": PORT_OPACITY,
        "fill_opacity": PORT_OPACITY
    }

    # 와이어 관련 설정
    WIRE_COLOR = YELLOW
    WIRE_STROKE_WIDTH = 2
    WIRE_OPACITY = 0.8

    # 도형 위치 조정 관련 상수
    CIRCLE_OFFSET_RATIO = 0.025  # 원의 오프셋 비율 (size * CIRCLE_OFFSET_RATIO)

    # 좌표 변환 관련 상수
    DEFAULT_Z_COORD = 0  # 기본 z좌표값

    # AND 게이트 관련 상수 추가
    AND_GATE_WIDTH_RATIO = 0.3     # 전체 크기 대비 사각형 부분 너비 비율
    AND_GATE_ARC_RATIO = 0.5      # 전체 크기 대비 반원 반지름 비율
