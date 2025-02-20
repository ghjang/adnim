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

    # OR 게이트 관련 상수 수정
    OR_GATE_WIDTH_RATIO = 0.25      # 너비 비율 조정 (조금 더 좁게)
    OR_GATE_CURVE_DEPTH = 0.2       # 곡선의 깊이 증가
    # 입력 포트 간격 비율 (기존 PORT_VERTICAL_SPACING의 1.9배)
    OR_GATE_PORT_SPACING = 1.9

    # NAND 게이트 관련 상수
    NAND_GATE_CIRCLE_RATIO = 0.08      # 출력 원의 크기 비율
    NAND_GATE_CIRCLE_OFFSET = 0.01     # 출력 원의 이격 거리 비율 (0.05 -> 0.01로 축소)

    # NOR 게이트 관련 상수
    NOR_GATE_CIRCLE_RATIO = 0.08      # 출력 원의 크기 비율 (NAND와 동일)
    NOR_GATE_CIRCLE_OFFSET = 0.01     # 출력 원의 이격 거리 비율 (NAND와 동일)

    # XOR 게이트 관련 상수 수정
    XOR_GATE_WIDTH_RATIO = 0.25        # OR 게이트와 동일한 너비 비율
    XOR_GATE_CURVE_DEPTH = 0.2         # OR 게이트와 동일한 곡선 깊이
    XOR_GATE_PORT_SPACING = 1.9        # OR 게이트와 동일한 포트 간격
    XOR_GATE_EXTRA_CURVE_OFFSET = 0.08  # 추가 곡선의 오프셋 비율 (0.15 -> 0.08로 축소)
    XOR_GATE_EXTRA_CURVE_WIDTH = 3.0   # 추가 곡선의 선 두께
