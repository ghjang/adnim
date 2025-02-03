from manim import *
from exercise.ch_01_02 import factorize, factors_to_latex
from collections import deque
import numpy as np

# 전역 상수
# TARGET_NUMBER = 100
# TARGET_NUMBER = 360
TARGET_NUMBER = 5083
NODE_RADIUS = 0.5
ARROW_TIP_LENGTH = 0.15
ARROW_COLOR = YELLOW
H_SPREAD = 2
ARROW_THICKNESS = 4

# 화면 여백 상수
H_MARGIN = 1.0
V_MARGIN_BOTTOM = 1.0
V_MARGIN_TOP = 0.5

# 트리 노드 클래스


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.pos = None


# 수정된 build_factor_tree: 미리 계산된 factor 리스트를 인자로 받을 수 있음.
def build_factor_tree(n: int, factors: list = None) -> TreeNode:
    if factors is None:
        factors = factorize(n)
    queue = deque([TreeNode(f) for f in factors])
    if not queue:
        return TreeNode(n)
    while len(queue) > 1:
        left = queue.popleft()
        right = queue.popleft()
        parent = TreeNode(left.value * right.value, left, right)
        queue.append(parent)
    return queue[0]


def get_tree_height(root: TreeNode) -> int:
    if not root:
        return 0
    return 1 + max(get_tree_height(root.left), get_tree_height(root.right))


def assign_positions(root: TreeNode, pos, dx, dy):
    """
    재귀적으로 각 노드에 위치를 할당.
    pos: 현재 노드의 위치, dx: 수평 간격, dy: 수직 간격.
    """
    if not root:
        return
    root.pos = pos
    if root.left:
        assign_positions(root.left, pos + LEFT * dx + DOWN * dy, dx/2, dy)
    if root.right:
        assign_positions(root.right, pos + RIGHT * dx + DOWN * dy, dx/2, dy)


def create_node(text, pos):
    """원과 텍스트를 묶어 하나의 노드(VGroup)로 반환"""
    circle = Circle(radius=NODE_RADIUS, color=BLUE)
    txt = Text(text, font_size=24)
    node = VGroup(circle, txt)
    txt.move_to(circle.get_center())
    node.move_to(pos)
    return node


class FactorizationTreeAnimation(Scene):
    def construct(self):
        # 미리 factorize를 한 번 호출
        factors = factorize(TARGET_NUMBER)
        tree_root = build_factor_tree(TARGET_NUMBER, factors)
        height = get_tree_height(tree_root)

        # 화면 크기와 여백을 고려한 동적 간격 계산
        frame_width = config.frame_width
        frame_height = config.frame_height
        effective_width = frame_width - H_MARGIN
        effective_height = frame_height - V_MARGIN_TOP - V_MARGIN_BOTTOM
        dynamic_dy = effective_height / height
        dynamic_H_spread = H_SPREAD * (height / 4)
        # 기존 dynamic_dx 계산과 효과적인 horizontal 여백을 고려하여 제한
        dynamic_dx_candidate = dynamic_H_spread * \
            effective_width / (2**(height-1))
        dynamic_dx = min(dynamic_dx_candidate, effective_width/4)
        dynamic_root_pos = UP * (effective_height/2)

        assign_positions(tree_root, dynamic_root_pos,
                         dx=dynamic_dx, dy=dynamic_dy)

        node_mapping = {}
        root_mobj = create_node(str(tree_root.value), tree_root.pos)
        node_mapping[tree_root] = root_mobj
        self.play(FadeIn(root_mobj), run_time=0.5)
        current_level = [tree_root]
        self.wait(0.5)

        while current_level:
            next_level = []
            edge_anims = []
            new_node_anims = []
            for node in current_level:
                parent_mobj = node_mapping[node]
                for child in (node.left, node.right):
                    if child is not None:
                        child_mobj = create_node(str(child.value), child.pos)
                        node_mapping[child] = child_mobj
                        parent_center = parent_mobj.get_center()
                        child_center = child_mobj.get_center()
                        direction = (child_center - parent_center) / \
                            np.linalg.norm(child_center - parent_center)
                        start_point = parent_center + direction * NODE_RADIUS
                        end_point = child_center - direction * NODE_RADIUS
                        arrow = Arrow(
                            start=start_point,
                            end=end_point,
                            buff=0,
                            tip_length=ARROW_TIP_LENGTH,
                            color=ARROW_COLOR,
                            stroke_width=ARROW_THICKNESS
                        )
                        edge_anims.append(Create(arrow, run_time=0.5))
                        next_level.append(child)
                        new_node_anims.append(FadeIn(child_mobj, run_time=0.5))
            if edge_anims:
                self.play(*edge_anims)
            if new_node_anims:
                self.play(*new_node_anims)
            current_level = next_level
            self.wait(0.5)

        result_str = f"{TARGET_NUMBER} = " + factors_to_latex(factors)
        result_text = MathTex(result_str, font_size=64)
        result_text.to_edge(DOWN)
        self.play(FadeIn(result_text))
        self.wait(2)
