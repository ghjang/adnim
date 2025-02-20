from abc import ABC, abstractmethod
from typing import List
import numpy as np
from manim import Dot, ManimColor


class LogicGateBase(ABC):
    """논리 게이트 기본 인터페이스"""
    size: float
    color: ManimColor
    input_ports: List[Dot]
    output_ports: List[Dot]

    @abstractmethod
    def get_input_point(self, index: int = 0) -> np.ndarray: pass

    @abstractmethod
    def get_output_point(self, index: int = 0) -> np.ndarray: pass

    @abstractmethod
    def update_connected_wires(self) -> None: pass


class WireBase(ABC):
    """와이어 기본 인터페이스"""
    @abstractmethod
    def set_start_gate(self, gate: LogicGateBase,
                       port_index: int) -> None: pass

    @abstractmethod
    def set_end_gate(self, gate: LogicGateBase, port_index: int) -> None: pass

    @abstractmethod
    def update_start_position(self) -> None: pass

    @abstractmethod
    def update_end_position(self) -> None: pass
