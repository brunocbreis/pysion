from typing import Protocol


class Curve(Protocol):
    KEYFRAMES: int

    def compute(self):
        """Computes the values of the curve"""


class EaseInOut:
    KEYFRAMES: int = 2

    def __init__(
        self,
        start_frame: int,
        end_frame: int,
        start_value: float,
        end_value: float,
        intensity: float = 1 / 3,
    ) -> None:
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.start_value = start_value
        self.end_value = end_value
        self.intensity = intensity

    def compute(self):
        ...


class Linear:
    KEYFRAMES: int = 2

    def __init__(
        self, start_frame: int, end_frame: int, start_value: float, end_value: float
    ) -> None:
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.start_value = start_value
        self.end_value = end_value

    def compute(self):
        ...
