from manim import *
from common.enhanced_number_plane import EnhancedNumberPlane


class ParabolaExample(Scene):
    def construct(self):
        plane = EnhancedNumberPlane()
        self.add(plane)
