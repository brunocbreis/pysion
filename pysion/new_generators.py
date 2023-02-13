from __future__ import annotations
from collections import UserDict, UserList


class NamedDict(UserDict):
    def __init__(
        self, name: str, dict: NamedDict = None, /, force_indent=False, **kwargs
    ):
        self.name = name
        self.level = 1
        self.force_indent = force_indent

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
        if len(self) == 1 and not self.force_indent:
            lvl = 0

        self.level = lvl

        ind0: str = "" if not lvl else "\t" * (lvl - 1)
        ind1: str = ind0 if not lvl else "\t" * lvl
        br = "\n" if lvl else ""

        s = self.name + " { " + br

        for k, v in self.data.items():
            match v:
                case str():
                    v = qs(v)
                case NamedDict():
                    v = v.render(lvl + 1)
                case list():
                    if len(v) > 1:
                        v = IndentedList(lvl + 1, v)
                    v = repr(v).replace("[", "{ ").replace("]", " }")
                case tuple():
                    v = repr(v).replace("(", "{ ").replace(")", " }")
                case None:
                    continue

            s += f"{ind1}{k} = {v}, {br}"

        s += ind0 + "}"

        return s


class UnnamedDict(NamedDict):
    def __init__(self, dict: NamedDict = None, /, force_indent=False, **kwargs):
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
                    i = qs(i)
                case NamedDict():
                    i = i.render(self.level + 1)
                case list():
                    if len(i) > 1:
                        i = IndentedList(self.level + 1, i)
                    i = repr(i).replace("[", "{ ").replace("]", " }")
                case tuple():
                    i = repr(i).replace("(", "{ ").replace(")", " }")
                case None:
                    continue

            s += f"{ind1}{i},\n"

        s += f"{ind0}]"

        return s


# aliases
ud = UnnamedDict
nd = NamedDict

# quoted string
def qs(string: str) -> str:
    return f'"{string}"'
