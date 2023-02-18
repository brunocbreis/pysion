from __future__ import annotations
from ..named_table import NamedTable, UnnamedTable
from dataclasses import dataclass
from .keyframe import Keyframe
from .curve import Curve


@dataclass
class BezierSpline:
    name: str

    def __post_init__(self):
        self.id = "BezierSpline"
        self.keyframes: UnnamedTable[int | float, Keyframe] = UnnamedTable()

    def add_keyframes(
        self,
        pairs: list[tuple[int | float, int | float]],
        curve: Curve = Curve.linear(),
    ) -> BezierSpline:
        if not pairs:
            return self

        if len(pairs) == 1:
            kf = Keyframe(*pairs[0])
            self.keyframes[kf.frame] = kf.value

            return self

        if curve == Curve():
            for pair in pairs:
                kf = Keyframe(*pair)
                self.keyframes[kf.frame] = kf.value
            return self

        for i, pair in enumerate(sorted(pairs, key=lambda x: x[0])):
            if i == 0:
                # rh only
                next_frame, next_value = pairs[i + 1]

                kf = Keyframe(*pair)

                rh_x = kf.frame + (next_frame - kf.frame) * curve.right_hand[0]
                rh_y = kf.value + (next_value - kf.value) * curve.right_hand[1]

                kf.right_hand = (rh_x, rh_y)

                self.keyframes[kf.frame] = kf
                continue

            if i == len(pairs) - 1:
                # lh only
                previous_frame, previous_value = pairs[i - 1]

                kf = Keyframe(*pair)

                lh_x = kf.frame - (kf.frame - previous_frame) * curve.right_hand[0]
                lh_y = kf.value - (kf.value - previous_value) * curve.right_hand[1]

                kf.left_hand = (lh_x, lh_y)

                self.keyframes[kf.frame] = kf
                continue

            next_frame, next_value = pairs[i + 1]
            previous_frame, previous_value = pairs[i - 1]

            kf = Keyframe(*pair)

            rh_x = kf.frame + (next_frame - kf.frame) * curve.right_hand[0]
            rh_y = kf.value + (next_value - kf.value) * curve.right_hand[1]

            lh_x = kf.frame - (kf.frame - previous_frame) * curve.right_hand[0]
            lh_y = kf.value - (kf.value - previous_value) * curve.right_hand[1]

            kf.right_hand = (rh_x, rh_y)
            kf.left_hand = (lh_x, lh_y)

            self.keyframes[kf.frame] = kf

        return self

    def _render_keyframes(self) -> UnnamedTable:
        keyframes_unnamed_table = UnnamedTable()
        for frame, keyframe in self.keyframes.items():
            keyframes_unnamed_table[frame] = keyframe

        return keyframes_unnamed_table

    def render(self) -> NamedTable:
        keyframes_unnamed_table = self._render_keyframes()

        return NamedTable(self.id, KeyFrames=keyframes_unnamed_table)
