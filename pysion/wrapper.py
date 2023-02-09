from typing import Protocol
from .utils import fusion_point, fusion_coords


class Operator(Protocol):
    @property
    def name(self) -> str:
        pass

    @property
    def string(self) -> str:
        pass

    @property
    def position(self) -> tuple[int, int]:
        pass

    @property
    def id(self) -> str:
        pass


def wrap_for_fusion(operators: list[Operator]) -> str:
    """Adds header and footer to a sequence of tools"""

    ops_string = "".join([op.string for op in operators])

    header = "{\n\tTools = ordered() {\n"
    footer = f'\t}},\n\tActiveTool = "{operators[-1].name}"\n}}'

    return header + ops_string + footer


def wrap_for_macro(macro: Operator, inputs: str, outputs: str, tools: list[Operator]):
    header = f"\t\t{macro.name} = {macro.id} {{" f"\n\t\t\tInputs = ordered() {{"

    joint1 = "\n\t\t\t},\n\t\t\tOutputs = {"

    joint2 = f"\n\t\t\t}},\n\t\t\tViewInfo = GroupInfo {{ Pos = {fusion_point(*fusion_coords(macro.position))}, }},"

    footer = "\n\t\t},"

    return header + inputs + joint1 + outputs + joint2 + wrap_tools(tools) + footer


def wrap_tools(tools: list[Operator]) -> str:
    tools_str = "\n".join([tool.string for tool in tools])

    return f"\n\t\t\tTools = ordered() {{ \n\t\t\t\t{tools_str} \t\t\t\t}},"
