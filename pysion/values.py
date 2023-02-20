from collections import UserList

"""This module deals with how values should be displayed in Fusion code."""


class FuID(UserList):
    def __init__(self, name: str) -> None:
        return super().__init__([name])

    def __repr__(self) -> str:
        return "FuID " + super().__repr__().replace("[", "{ ").replace(
            "]", " }"
        ).replace("'", '"')


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
