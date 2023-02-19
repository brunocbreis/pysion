from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Curve:
    left_hand: tuple[float, float] | None = None
    right_hand: tuple[float, float] | None = None
    name: str = ""

    def __repr__(self) -> str:
        LH = self.left_hand
        RH = self.right_hand

        name = "" if not self.name else f"{self.name} "

        return f"{name}Curve({LH=}, {RH=})"

    @classmethod
    def ease_in(cls, strength: float = 1 / 3) -> Curve:
        return Curve((strength, 0), None, "Ease in")

    @classmethod
    def ease_out(cls, strength: float = 1 / 3) -> Curve:
        return Curve(None, (strength, 0), "Ease out")

    @classmethod
    def ease_in_and_out(cls, strength: float = 1 / 3) -> Curve:
        return Curve((strength, 0), (strength, 0), "Ease In and Out")

    @classmethod
    def decelerate_in(cls, strength: float = 1) -> Curve:
        return Curve((0, strength), None, "Decelerate in")

    @classmethod
    def decelerate_out(cls, strength: float = 1) -> Curve:
        return Curve(None, (0, strength), "Decelerate out")

    @classmethod
    def decelerate_in_and_out(cls, strength: float = 1) -> Curve:
        return Curve((0, strength), (0, strength), "Decelerate in and out")

    @classmethod
    def flat(cls) -> Curve:
        return Curve.ease_in_and_out()

    @classmethod
    def linear(cls) -> Curve:
        return Curve(name="Linear")

    @classmethod
    def smooth(cls) -> Curve:
        # TODO: the Y is affected by the X... how to implement?
        return Curve()
