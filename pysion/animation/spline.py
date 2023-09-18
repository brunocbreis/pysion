from __future__ import annotations
from ..named_table import NamedTable, UnnamedTable
from dataclasses import dataclass
from .keyframe import Keyframe
from .curve import Curve
from ..color import RGBA


@dataclass
class BezierSpline:
    name: str
    default_curve: Curve = None
    color: RGBA | None = None

    def __post_init__(self):
        self.id = "BezierSpline"
        self.keyframes: UnnamedTable[int | float, Keyframe] | None = None

        if self.default_curve is None:
            self.default_curve = Curve.linear()

    def __setitem__(self, key: int | float, value: int | float | str) -> None:
        assert isinstance(key, int) | isinstance(key, float), "Frame must be a number."
        self.add_keyframes([(key, value)], self.default_curve)

    def __getitem__(self, key: int | float) -> Keyframe:
        return self.keyframes[key]

    def render(self) -> NamedTable:
        keyframes = self._render_keyframes()
        color = self._render_color()

        return NamedTable(self.id, KeyFrames=keyframes, SplineColor=color)

    def __repr__(self) -> str:
        return repr(self.render())

    def add_keyframes(
        self,
        pairs: list[tuple[int | float, int | float | str]],
        curve: Curve | None = None,
    ) -> BezierSpline:
        if not pairs:
            return self

        if curve is None:
            curve = self.default_curve

        for pair in pairs:
            kf = Keyframe(*pair, curve)
            self._add_keyframe(kf)

        return self

    def apply_curve(self, curve: Curve) -> None:
        """Applies the same curve to all existing keyframes. Overrides previously set curves."""

        if not self.keyframes:
            print(f"No keyframes have been added. Setting default curve to {curve}")
            self.default_curve = curve
            return None

        for keyframe in self.keyframes.values():
            keyframe.add_curve(curve)

    def set_spline_color(self, color: RGBA) -> None:
        self.color = color

    # Private methods
    def _add_keyframe(self, kf: Keyframe) -> None:
        if self.keyframes is None:
            self.keyframes = UnnamedTable()

        self.keyframes[kf.frame] = kf

    def _calculate_hands(self) -> None:
        if not self.keyframes:
            return

        if len(self.keyframes) == 1:
            return

        keyframes: list[tuple[int | float, Keyframe]] = self.keyframes.as_ordered_list()
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

    def _render_keyframes(self) -> UnnamedTable | None:
        if not self.keyframes:
            return None

        self._calculate_hands()
        ordered_keyframes = UnnamedTable()

        for frame, keyframe in self.keyframes.as_ordered_list():
            ordered_keyframes[frame] = keyframe

        return ordered_keyframes

    def _render_color(self) -> UnnamedTable | None:
        if not self.color:
            return None

        return UnnamedTable(
            Red=int(self.color.red * 255),
            Green=int(self.color.green * 255),
            Blue=int(self.color.blue * 255),
            force_unindent=True,
        )
