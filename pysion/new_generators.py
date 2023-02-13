from __future__ import annotations
from luadata import serialize
from dataclasses import dataclass, field
from collections import UserDict


def named_table(
    name: str, type: str, content: dict[str, int | float | str | list[float]] = None
) -> str:
    if not content:
        content = {}

    ind = "\t" if len(content) > 1 else None
    ind_lvl = 0

    return f"{name} = {type} {serialize(content, indent=ind, indent_level=ind_lvl)},"


nt = named_table


def unnamed_table(
    type: str, content: dict[str, int | float | str | list[float]] = None
) -> str:
    if not content:
        content = {}

    ind = "\t" if len(content) > 1 else None
    ind_lvl = 0

    return f"{type} {serialize(content, indent=ind, indent_level=ind_lvl)},"


ut = unnamed_table


def ll(vals: list[float]) -> str:
    return repr(vals).replace("[", "{ ").replace("]", " },")


# @dataclass
# class Table:
#     name: str | None
#     kind: str | None
#     content: dict[str, int | float | str | list[float] | Table] = field(
#         default_factory=dict
#     )

#     def render(self) -> str:
#         ind_char = "\t"
#         lvl = 0

#         ind = "\n" + ind_char * lvl

#         name = "" if not self.name else f"{self.name} = "
#         kind = "" if not self.kind else self.kind

#         content = []

#         return f"{name}{kind}{content}"

#         ...


@dataclass
class Table:
    name: str
    value: Table | int | float | str | list[float] | list[Table]
    kind: str = ""

    def __str__(self) -> str:
        if self.kind or isinstance(self.value, Table):
            self.value = f" {{ {self.value}, }}"

        return f"{self.name} = {self.kind}{self.value}"


class NamedDict(UserDict):
    def __init__(self, name: str, dict: NamedDict = None, **kwargs):
        self.name = name
        super().__init__(dict, **kwargs)
        if dict is not None:
            self.update(dict)

    def __repr__(self) -> str:
        return self.render()

    def render(self, lvl: int = 1) -> str:
        if len(self) == 1:
            lvl = 0

        ind0: str = "" if not lvl else "\t" * (lvl - 1)
        ind1: str = ind0 if not lvl else "\t" * lvl
        br = "\n" if lvl else ""

        s = self.name + " { " + br

        for k, v in self.data.items():
            if isinstance(v, str):
                v = qs(v)
            if isinstance(v, NamedDict):
                v = v.render(lvl + 1)
            if isinstance(v, list):
                v = repr(v).replace("[", "{ ").replace("]", " }")
            if isinstance(v, tuple):
                v = repr(v).replace("(", "{ ").replace(")", " }")

            s += f"{ind1}{k} = {v}, {br}"

        s += ind0 + "}"

        return s


# quoted string
def qs(string: str) -> str:
    return f'"{string}"'
