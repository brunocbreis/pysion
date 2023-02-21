from __future__ import annotations
from collections import UserList


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
