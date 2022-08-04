from dataclasses import dataclass, field
from typing import Protocol


class Curve(Protocol):
    KEYFRAMES: int

    def compute(self):
        """Computes the values of the curve"""


class EaseInOut:
    def __init__(
        self,
        start_frame: int,
        end_frame: int,
        start_value: float,
        end_value: float,
        intensity: float = 1 / 3,
    ) -> None:
        self.keyframes: list[int] = []
        self.keyframes.append(start_frame)
        self.keyframes.append(end_frame)

        self.values: list[float] = []
        self.values.append(start_value)
        self.values.append(end_value)

        self.intensity = intensity

        self._right_handles: list[tuple[float, float]] = None
        self._left_handles: list[tuple[float, float]] = None

        self.compute()

    def compute(self):
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
        kf = add_keyframe_manual(
            self.keyframes[0], self.values[0], right_handle=self._right_handles[0]
        )
        return kf

    def last_keyframe(self) -> str:
        kf = add_keyframe_manual(
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
    KEYFRAMES: int = 2

    def __init__(
        self, start_frame: int, end_frame: int, start_value: float, end_value: float
    ) -> None:
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.start_value = start_value
        self.end_value = end_value
        self.intensity = 1

    def compute(self):
        ...


# animations
def add_spline(
    tool_name: str,
    input_name: str,
    spline_color: tuple[int, int, int] = (255, 0, 255),
    keyframes: str = "",
) -> str:
    """Creates a spline for an input in a tool."""
    r, g, b = spline_color

    spline = (
        f"\t\t{tool_name}{input_name} = BezierSpline {{\n\t\t\t"
        f"SplineColor = {{ Red = {r}, Green = {g}, Blue = {b} }},"
        f"\n\t\t\tKeyFrames = {{\n{keyframes}\t\t\t}}\n\t\t}},\n"
    )
    return spline


def add_spline(
    tool_name: str,
    input_name: str,
    animation: Curve,
    spline_color: tuple[int, int, int] = (255, 0, 255),
) -> str:
    """Creates a spline for an input in a tool."""
    r, g, b = spline_color
    keyframes = animation.generate()
    spline = (
        f"\t\t{tool_name}{input_name} = BezierSpline {{\n\t\t\t"
        f"SplineColor = {{ Red = {r}, Green = {g}, Blue = {b} }},"
        f"\n\t\t\tKeyFrames = {{\n{keyframes}\t\t\t}}\n\t\t}},\n"
    )
    return spline


def add_keyframe_manual(
    frame: int,
    value: float,
    left_handle: tuple[float, float] = "",
    right_handle: tuple[float, float] = "",
) -> str:
    if left_handle:
        left_x, left_y = left_handle
        left_handle = f"LH = {{ {left_x}, {left_y} }}, "

    if right_handle:
        right_x, right_y = right_handle
        right_handle = f"RH = {{ {right_x}, {right_y} }} "

    kf = f"\t\t\t\t[{frame}] = {{ {value}, {left_handle}{right_handle}}},\n"

    return kf


def calc_ease_out(
    frames: tuple[int, int],
    values: tuple[float, float],
    intensity: float = 1 / 3,
) -> tuple[float, float]:
    """Returns the right handle coords of the first keyframe as a tuple (x, y)"""

    t0, t1 = frames
    v0, v1 = values

    x_offset = t0
    x_amp = t1 - t0

    x = x_offset + intensity * x_amp
    y = v0
    return x, y


def calc_ease_in(
    frames: tuple[int, int],
    values: tuple[float, float],
    intensity: float = 1 / 3,
) -> tuple[float, float]:
    """Returns the right handle coords of the first keyframe as a tuple (x, y)"""

    t0, t1 = frames
    v0, v1 = values

    x_offset = t0
    x_amp = t1 - t0

    x = t1 - intensity * x_amp
    y = v1
    return x, y


def animate(
    frames: tuple[int, int],
    values: tuple[float, float],
    ease: tuple[float, float] = (1 / 3, 1 / 3),
) -> str:
    """Creates eased keyframes"""
    ease_in = calc_ease_in(frames, values, ease[0])
    ease_out = calc_ease_out(frames, values, ease[1])

    kfs = add_keyframe_manual(
        frames[0], values[0], right_handle=ease_out
    ) + add_keyframe_manual(frames[1], values[1], left_handle=ease_in)

    return kfs


# so what i have to do is
#
