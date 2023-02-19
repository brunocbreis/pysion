from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Curve:
    left_hand: tuple[float, float] | None = None
    right_hand: tuple[float, float] | None = None

    @classmethod
    def ease_in(cls, strength: float = 1 / 3) -> Curve:
        return Curve((strength, 0), None)

    @classmethod
    def ease_out(cls, strength: float = 1 / 3) -> Curve:
        return Curve(None, (strength, 0))

    @classmethod
    def ease_in_and_out(cls, strength: float = 1 / 3) -> Curve:
        return Curve((strength, 0), (strength, 0))

    @classmethod
    def flat(cls) -> Curve:
        return Curve.ease_in_and_out()

    @classmethod
    def linear(cls) -> Curve:
        return Curve()

    @classmethod
    def smooth(cls) -> Curve:
        # TODO: the Y is affected by the X... how to implement?
        return Curve()
