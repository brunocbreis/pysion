from __future__ import annotations
from collections import UserList

"""This module deals with how values should be displayed in Fusion code."""


class FuID(UserList):
    def __init__(self, name: str) -> None:
        return super().__init__([name])

    def __repr__(self) -> str:
        return "FuID " + super().__repr__().replace("[", "{ ").replace(
            "]", " }"
        ).replace("'", '"')

    # Filters
    @classmethod
    def fast_gaussian(cls) -> FuID:
        return FuID("Fast Gaussian")

    @classmethod
    def gaussian(cls) -> FuID:
        return FuID("Gaussian")

    @classmethod
    def multi_box(cls) -> FuID:
        return FuID("Multi-box")

    @classmethod
    def box(cls) -> FuID:
        return FuID("Box")

    @classmethod
    def bartlett(cls) -> FuID:
        return FuID("Bartlett")

    # Paint mode
    @classmethod
    def merge(cls) -> FuID:
        return FuID("Merge")

    @classmethod
    def add(cls) -> FuID:
        return FuID("Add")

    @classmethod
    def subtract(cls) -> FuID:
        return FuID("Subtract")

    @classmethod
    def minimum(cls) -> FuID:
        return FuID("Minimum")

    @classmethod
    def maximum(cls) -> FuID:
        return FuID("Maximum")

    @classmethod
    def average(cls) -> FuID:
        return FuID("Average")

    @classmethod
    def multiply(cls) -> FuID:
        return FuID("Multiply")

    @classmethod
    def replace(cls) -> FuID:
        return FuID("Replace")

    @classmethod
    def invert(cls) -> FuID:
        return FuID("Invert")

    @classmethod
    def copy(cls) -> FuID:
        return FuID("Copy")

    @classmethod
    def ignore(cls) -> FuID:
        return FuID("Ignore")


# Display funcs
def quoted_string(string: str) -> str:
    return f'"{string}"'


def list_as_table(ls: list) -> str:
    return repr(ls).replace("[", "{ ").replace("]", " }")


def tuple_as_table(tp: tuple) -> str:
    return repr(tp).replace("(", "{ ").replace(")", " }")


def lowercase_bool(b: bool) -> str:
    return repr(b).lower()


def keyframe(n: int | float) -> str:
    return f"[{n}]"
