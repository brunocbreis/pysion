from __future__ import annotations
from collections import UserDict


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
                    v = repr(v).replace("[", "{ ").replace("]", " }")
                case tuple():
                    v = repr(v).replace("(", "{ ").replace(")", " }")

            s += f"{ind1}{k} = {v}, {br}"

        s += ind0 + "}"

        return s


class UnnamedDict(NamedDict):
    def __init__(self, dict: NamedDict = None, /, force_indent=False, **kwargs):
        super().__init__("", dict, force_indent=force_indent, **kwargs)


# aliases
ud = UnnamedDict
nd = NamedDict

# quoted string
def qs(string: str) -> str:
    return f'"{string}"'
