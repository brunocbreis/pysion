from typing import Protocol
from ..named_table import NamedTable, UnnamedTable


def add_keyframe(
    frame: int | float,
    value: int | float,
    left_handle: tuple[float, float] | None = None,
    right_handle: tuple[float, float] | None = None,
) -> str:
    if left_handle:
        left_x, left_y = left_handle
        left_handle = f"LH = {{ {left_x}, {left_y} }}, "

    if right_handle:
        right_x, right_y = right_handle
        right_handle = f"RH = {{ {right_x}, {right_y} }} "

    kf = UnnamedTable

    kf = f"\t\t\t\t[{frame}] = {{ {value}, {left_handle}{right_handle}}},\n"

    return kf


class Curve(Protocol):
    def compute(self) -> None:
        """Computes the values of the curve"""

    def first_keyframe(self) -> str:
        ...

    def middle_keyframes(self) -> str:
        ...

    def last_keyframe(self) -> str:
        ...

    def generate(self) -> str:
        """Returns a string with the generated curve in Fusion language"""
        return self.first_keyframe() + self.middle_keyframes() + self.last_keyframe()


class EaseInOut:
    def __init__(
        self,
        start_frame: int,
        end_frame: int,
        start_value: float,
        end_value: float,
        intensity: float = 1 / 3,
    ) -> None:
        self.keyframes: list[int] = [start_frame, end_frame]
        self.values: list[float] = [start_value, end_value]

        self.intensity = intensity

        self._right_handles: list[tuple[float, float]] = None
        self._left_handles: list[tuple[float, float]] = None

        self.compute()

    def compute(self) -> None:
        if self._right_handles is None:
            self._right_handles = []
        if self._left_handles is None:
            self._left_handles = []

        right_handle = self.calc_ease_out()
        left_handle = self.calc_ease_in()
        self._right_handles.append(right_handle)
        self._left_handles.append(left_handle)
        ...

    def first_keyframe(self) -> str:
        kf = add_keyframe(
            self.keyframes[0], self.values[0], right_handle=self._right_handles[0]
        )
        return kf

    def last_keyframe(self) -> str:
        kf = add_keyframe(
            self.keyframes[-1], self.values[-1], left_handle=self._left_handles[-1]
        )
        return kf

    def middle_keyframes(self) -> str:
        if len(self.keyframes) <= 2:
            return ""
        return ""

    def calc_ease_out(self) -> tuple[float, float]:
        """Returns the right handle coords of the first keyframe as a tuple (x, y)"""

        t0, t1 = self.keyframes
        v0 = self.values[0]
        intensity = self.intensity

        x_offset = t0
        x_amp = t1 - t0

        x = x_offset + intensity * x_amp
        y = v0
        return x, y

    def calc_ease_in(self) -> tuple[float, float]:
        """Returns the left handle coords of the second keyframe as a tuple (x, y)"""

        t0, t1 = self.keyframes
        v1 = self.values[1]
        intensity = self.intensity

        x_amp = t1 - t0

        x = t1 - intensity * x_amp
        y = v1
        return x, y

    def generate(self) -> str:
        return self.first_keyframe() + self.middle_keyframes() + self.last_keyframe()


class Linear:
    def __init__(
        self, start_frame: int, end_frame: int, start_value: float, end_value: float
    ) -> None:
        self.keyframes = [start_frame, end_frame]
        self.start_value = start_value
        self.end_value = end_value
        self.intensity = 1

    def compute(self):
        ...

    def first_keyframe(self):
        ...

    def middle_keyframes(self):
        ...

    def last_keyframe(self):
        ...

    def generate(self):
        """Returns a string with the generated curve in Fusion language"""


def kf_pairs(keyframes: list[int]) -> zip:
    return zip(keyframes, keyframes[1:])
