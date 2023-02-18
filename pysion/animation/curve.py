from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Curve:
    left_hand: tuple[float, float] | None = None
    right_hand: tuple[float, float] | None = None

    @classmethod
    def ease_in(cls) -> Curve:
        return Curve((1 / 3, 0))

    @classmethod
    def ease_out(cls) -> Curve:
        return Curve(None, (1 / 3, 0))

    @classmethod
    def ease_in_and_out(cls) -> Curve:
        return Curve((1 / 3, 0), (1 / 3, 0))

    @classmethod
    def linear(cls) -> Curve:
        return Curve()
