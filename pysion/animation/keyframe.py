from __future__ import annotations
from collections import UserDict
from ..named_table import tuple_as_table, UnnamedTable


class Keyframe(UserDict):
    def __init__(
        self,
        frame: int | float,
        value: int | float,
        right_hand: tuple[float, float] | None = None,
        left_hand: tuple[float, float] | None = None,
    ) -> None:
        self.frame = frame
        self.value = value

        self.loop: bool | None = None
        self.ping_pong: bool | None = None
        self.loop_rel: bool | None = None
        self.step_in: bool | None = None
        self.step_out: bool | None = None

        return super().__init__(RH=right_hand, LH=left_hand)

    def __repr__(self) -> str:
        hands = " "

        flags = self._render_flags()
        if flags is None:
            flags = ""

        for hand, value in self.data.items():
            if value is None:
                continue
            hands += f"{hand} = {tuple_as_table(value)}, "

        return f"{{ {self.value},{hands} }}"

    def add_flags(
        self,
        loop: bool | None = None,
        ping_pong: bool | None = None,
        loop_rel: bool | None = None,
        step_in: bool | None = None,
        step_out: bool | None = None,
    ) -> Keyframe:
        self.loop = loop
        self.ping_pong = ping_pong
        self.loop_rel = loop_rel
        self.step_in = step_in
        self.step_out = step_out

        return self

    def _render_flags(self) -> UnnamedTable | None:
        if any(self.loop, self.ping_pong, self.loop_rel, self.step_in, self.step_out):
            flags = UnnamedTable()
            flags["Loop"] = self.loop
            flags["PingPong"] = self.ping_pong
            flags["LoopRel"] = self.loop_rel
            flags["StepIn"] = self.step_in
            flags["StepOut"] = self.step_out

            return flags

        return None
