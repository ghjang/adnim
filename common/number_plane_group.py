import re  # 정규표현식 지원 추가
from manim import *

from .number_plane_group_impl.number_plane_group_base import (
    MobjectType,
    OriginStyle
)
from .number_plane_group_impl.basic_shape import BasicShapeMixin
from .number_plane_group_impl.label import LabelMixIn
from .number_plane_group_impl.function import FunctionPlotMixIn


class NumberPlaneGroup(BasicShapeMixin,
                       LabelMixIn,
                       FunctionPlotMixIn):
    def __init__(self,
                 x_range=[-20, 20, 1],
                 y_range=[-20, 20, 1],
                 x_length=16,
                 y_length=16,
                 axis_config={},
                 background_line_style={"stroke_opacity": 0.4},
                 origin_config=None,
                 **kwargs):
        all_params = {
            'x_range': x_range,
            'y_range': y_range,
            'x_length': x_length,
            'y_length': y_length,
            'axis_config': axis_config,
            'background_line_style': background_line_style,
            'origin_config': origin_config,
            **kwargs
        }
        super().__init__(**all_params)

    def get_origin_marker(self):
        """원점 마커 가져오기"""
        return self.find_mobject(None, MobjectType.ORIGIN)

    def set_origin_style(self, style_type, config=None):
        """원점 표시 스타일 변경"""
        if config is None:
            config = {
                "color": RED,
                "size": 0.1,
                "opacity": 1.0
            }

        # 기존 원점 표시 제거
        old_marker = self.get_origin_marker()
        if (old_marker):
            self.remove(old_marker)

        # 새로운 원점 표시 생성 및 추가
        new_marker = self._create_origin_marker(style_type, config)
        self.add(new_marker)

    def get_current_origin_style(self):
        """현재 원점 스타일 가져오기"""
        marker = self.get_origin_marker()
        return marker.metadata.get("style") if marker else None

    def show_origin(self, show=True):
        marker = self.get_origin_marker()
        if (marker):
            marker.set_opacity(1 if show else 0)

    def find_mobject(self, name, obj_type=None):
        """이름과 타입으로 객체 찾기"""
        for mob in self.submobjects:
            self._ensure_metadata(mob)
            if (mob.metadata.get("name") == name and
                    (obj_type is None or mob.metadata.get("type") == obj_type)):
                return mob
        return None

    def iter_mobjects(self, name_pattern=None, obj_type=None):
        """이름 패턴과 타입으로 객체들을 필터링하여 이터레이션

        Args:
            name_pattern (str, optional): 정규표현식 패턴 (예: "point_.*", "function_[0-9]+")
            obj_type (str, optional): 객체 타입 (예: "point", "function", "parametric")

        Yields:
            Mobject: 조건에 맞는 객체들
        """
        pattern = re.compile(name_pattern) if name_pattern else None

        for mob in self.submobjects:
            self._ensure_metadata(mob)

            # 타입 체크
            if obj_type and mob.metadata.get("type") != obj_type:
                continue

            # 이름 패턴 체크
            if pattern:
                name = mob.metadata.get("name")
                if not name or not pattern.match(name):
                    continue

            yield mob

    def get_all_points(self):
        """모든 점 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.POINT)

    def get_all_functions(self):
        """모든 함수 그래프 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.FUNCTION)

    def get_all_parametrics(self):
        """모든 파라메트릭 그래프 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.PARAMETRIC)

    def get_all_labels(self):
        """모든 라벨 객체 이터레이터"""
        return self.iter_mobjects(obj_type=MobjectType.LABEL)

    def remove_all_by_pattern(self, name_pattern, obj_type=None):
        """패턴과 타입에 맞는 모든 객체 제거"""
        for mob in list(self.iter_mobjects(name_pattern, obj_type)):
            self.remove(mob)

    def copy_with_transformed_plane(self, x_range=None, y_range=None,
                                    x_length=None, y_length=None, **kwargs):
        """좌표계 변환 복사 메서드 개선"""
        new_group = super().copy()
        new_group.submobjects.clear()  # 기존 submobjects 제거

        # background_line_style이 명시적으로 지정되지 않은 경우 원본의 스타일을 사용
        if 'background_line_style' not in kwargs:
            kwargs['background_line_style'] = self.plane.background_line_style

        # 새로운 평면 생성
        new_plane = NumberPlane(
            x_range=x_range or self.plane.x_range,
            y_range=y_range or self.plane.y_range,
            x_length=x_length or self.plane.x_length,
            y_length=y_length or self.plane.y_length,
            **kwargs
        )

        # 메타데이터 보존
        new_group._ensure_metadata(new_plane)
        new_group.plane = new_plane
        new_group.add(new_plane)

        # 원점 마커 복사
        self._copy_origin_marker(new_group)

        # 다른 객체들 복사
        self._copy_mobjects_with_transform(new_group)

        return new_group
