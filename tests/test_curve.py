from pysion.animation import Curve
import pytest


def test_curve_repr():
    decel_out = Curve.decelerate_out()

    assert repr(decel_out) == "Decelerate out Curve(LH=None, RH=(0, 1))"


def test_flat_curve():
    assert Curve.flat() == Curve.ease_in_and_out()


def test_smooth_curve():
    with pytest.raises(NotImplementedError):
        Curve.smooth()
