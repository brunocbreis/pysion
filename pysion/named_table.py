from __future__ import annotations
from collections import UserDict, UserList
from typing import Any
from enum import Enum


class NamedTable(UserDict):
    def __init__(
        self,
        name: str,
        dict: NamedTable = None,
        /,
        force_indent=False,
        force_unindent=False,
        **kwargs,
    ):
        self.name = name
        self.level = 1
        self.force_indent = force_indent
        if force_unindent:
            self.force_indent = False
        self.force_unindent = force_unindent

        super().__init__(dict, **kwargs)
        if dict is not None:
            self.update(dict)

    def __repr__(self) -> str:
        return self.render(self.level)

    def __len__(self) -> int:
        l = 0
        for v in self.values():
            if v is None:
                continue
            l += 1
        return l

    def render(self, lvl: int = 1) -> str:
        if self.must_indent():
            self.force_indent = True
            self.force_unindent = False

        unindent = False
        if (len(self) < 2 and not self.force_indent) or self.force_unindent:
            # print("Setting unindent to True")
            unindent = True

        self.level = lvl

        ind0: str = "" if not lvl else "\t" * (lvl - 1)
        ind1: str = ind0 if not lvl else "\t" * lvl
        br = "\n" if lvl else ""

        if unindent:
            ind0 = ind1 = br = ""

        name = self.name + " " if self.name else ""
        s = f"{name}{{ {br}"

        for k, v in self.data.items():
            match k:
                case int() | float():
                    k = keyframe(k)
            match v:
                case str():
                    v = quoted_string(v)
                case NamedTable() | UnnamedTable():
                    v = v.render(lvl + 1)
                case list():
                    if len(v) > 1:
                        v = IndentedList(lvl + 1, v)
                    v = list_as_table(v)
                case tuple():
                    v = tuple_as_table(v)
                case bool():
                    v = lowercase_bool(v)
                case dict():
                    v = UnnamedTable(v).render(lvl + 1)
                case Enum():
                    v = v.value
                case None:
                    continue

            s += f"{ind1}{k} = {v}, {br}"

        s += ind0 + "}"

        return s

    def must_indent(self) -> bool:
        if self.force_unindent:
            return False

        if len(self) >= 2:
            # print("Must indent because length is >= 2")
            return True

        for val in self.values():
            if isinstance(val, NamedTable):
                if len(val) >= 2:
                    # print("Must indent because length of contained NamedTable is >= 2.")
                    return True
                if val.must_indent():
                    # print("Must indent because contained NamedTable also must indent.")
                    return True
            if isinstance(val, list):
                if len(val) >= 2:
                    # print("Must indent because length of contained list is >= 2.")
                    return True

        # print("Doesn't need to indent.")
        return False

    def ordered(self, reverse: bool = False) -> list[tuple[str | int | float, Any]]:
        """Returns the NamedTable as a sorted list of tuple[key, val], by keys.
        Useful for a table of keyframes that need to be sorted by time."""

        if self.data is None:

            return None

        data_list = []

        for k, v in self.items():
            pair = (k, v)
            data_list.append(pair)

        data_list.sort(key=lambda x: x[0], reverse=reverse)

        return data_list


class UnnamedTable(NamedTable):
    def __init__(self, dict: NamedTable = None, /, force_indent=False, **kwargs):
        super().__init__("", dict, force_indent=force_indent, **kwargs)


class IndentedList(UserList):
    def __init__(self, lvl: int, initlist) -> None:

        self.level = lvl
        return super().__init__(initlist)

    def __repr__(self) -> str:
        ind0: str = "" if not self.level else "\t" * (self.level - 1)
        ind1: str = ind0 if not self.level else "\t" * self.level

        s = "[\n"
        for i in self:
            match i:
                case str():
                    i = quoted_string(i)
                case NamedTable():
                    i = i.render(self.level + 1)
                case list():
                    if len(i) > 1:
                        i = IndentedList(self.level + 1, i)
                    i = list_as_table(i)
                case tuple():
                    i = tuple_as_table(i)
                case bool():
                    i = lowercase_bool(i)
                case None:
                    continue

            s += f"{ind1}{i},\n"

        s += f"{ind0}]"

        return s


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
