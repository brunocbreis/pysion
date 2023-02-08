from typing import Protocol


class Operator(Protocol):
    @property
    def name(self) -> str:
        pass

    @property
    def string(self) -> str:
        pass


def wrap_for_fusion(operators: list[Operator]) -> str:
    """Adds header and footer to a sequence of tools"""

    ops_string = "".join([op.string for op in operators])

    header = "{\n\tTools = ordered() {\n"
    footer = f'\t}},\n\tActiveTool = "{operators[-1].name}"\n}}'

    return header + ops_string + footer
