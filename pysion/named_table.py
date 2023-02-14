from __future__ import annotations
from collections import UserDict, UserList


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

        unindent = False
        if (len(self) == 1 and not self.force_indent) or self.force_unindent:
            unindent = True

        self.level = lvl

        ind0: str = "" if not lvl else "\t" * (lvl - 1)
        ind1: str = ind0 if not lvl else "\t" * lvl
        br = "\n" if lvl else ""

        if unindent:
            ind0 = ind1 = br = ""

        s = f"{self.name} {{ {br}"

        for k, v in self.data.items():
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
                case None:
                    continue

            s += f"{ind1}{k} = {v}, {br}"

        s += ind0 + "}"

        return s


class UnnamedTable(NamedTable):
    def __init__(self, dict: NamedTable = None, /, force_indent=False, **kwargs):
        super().__init__("", dict, force_indent=force_indent, **kwargs)

    def render(self, lvl: int = 1) -> str:
        print("Rendering unnamed table...")
        return super().render(lvl)


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
                case None:
                    continue

            s += f"{ind1}{i},\n"

        s += f"{ind0}]"

        return s


# Display funcs
def quoted_string(string: str) -> str:
    return f'"{string}"'


def list_as_table(ls: list) -> str:
    return repr(ls).replace("[", "{ ").replace("]", " }")


def tuple_as_table(tp: tuple) -> str:
    return repr(tp).replace("(", "{ ").replace(")", " }")
