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
        self.keyframes: UnnamedTable[int | float, Keyframe] | None = None

    def render(self) -> NamedTable:
        keyframes = self._render_keyframes()

        return NamedTable(self.id, KeyFrames=keyframes)

    def add_keyframes(
        self,
        pairs: list[tuple[int | float, int | float]],
        curve: Curve = Curve.linear(),
    ) -> BezierSpline:
        if not pairs:
            return self

        for pair in pairs:
            kf = Keyframe(*pair, curve)
            self._add_keyframe(kf)

        return self

    # Private methods
    def _add_keyframe(self, kf: Keyframe) -> None:
        if self.keyframes is None:
            self.keyframes = UnnamedTable()

        self.keyframes[kf.frame] = kf

    def _calculate_hands(self) -> UnnamedTable | None:
        if not self.keyframes:
            return None

        if len(self.keyframes) == 1:
            return self.keyframes

        keyframes: list[tuple[int | float, Keyframe]] = self.keyframes.ordered()
        for i, (frame, kf) in enumerate(keyframes):
            if i == 0:
                # rh only
                if kf.rel_right_hand is None:
                    continue

                next_frame, next_value = (
                    keyframes[i + 1][1].frame,
                    keyframes[i + 1][1].value,
                )

                rh_x = frame + (next_frame - frame) * kf.rel_right_hand[0]
                rh_y = kf.value + (next_value - kf.value) * kf.rel_right_hand[1]

                kf.right_hand = (rh_x, rh_y)
                continue

            if i == len(keyframes) - 1:
                # lh only
                if kf.rel_left_hand is None:
                    continue

                previous_frame, previous_value = (
                    keyframes[i - 1][1].frame,
                    keyframes[i - 1][1].value,
                )

                lh_x = frame - (frame - previous_frame) * kf.rel_left_hand[0]
                lh_y = kf.value - (kf.value - previous_value) * kf.rel_left_hand[1]

                kf.left_hand = (lh_x, lh_y)
                continue

            # both hands
            if kf.rel_right_hand is not None:
                next_frame, next_value = (
                    keyframes[i + 1][1].frame,
                    keyframes[i + 1][1].value,
                )
                rh_x = frame + (next_frame - frame) * kf.rel_right_hand[0]
                rh_y = kf.value + (next_value - kf.value) * kf.rel_right_hand[1]
                kf.right_hand = (rh_x, rh_y)

            if kf.rel_left_hand is not None:
                previous_frame, previous_value = (
                    keyframes[i - 1][1].frame,
                    keyframes[i - 1][1].value,
                )
                lh_x = frame - (frame - previous_frame) * kf.rel_left_hand[0]
                lh_y = kf.value - (kf.value - previous_value) * kf.rel_left_hand[1]

                kf.left_hand = (lh_x, lh_y)

        return self.keyframes

    def _render_keyframes(self) -> UnnamedTable | None:
        return self._calculate_hands()
