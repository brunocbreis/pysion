from __future__ import annotations
from dataclasses import dataclass
from .named_table import NamedTable, UnnamedTable
from .tool import Tool
from .macro import Macro
from typing import Protocol
from .input import Input


@dataclass
class Composition:
    """Represents a Fusion composition. Outputs an UnnamedTable with tool names as keys and tools as NamedTables."""

    tools: list[Operator] | None = None
    active_tool: Operator | None = None

    def __post_init__(self):
        if not self.active_tool:
            if self.tools:
                self.active_tool = self.tools[-1]

    def render(self) -> UnnamedTable:
        tools = UnnamedTable(
            {tool.name: tool.render() for tool in self.tools}, force_indent=True
        )

        return UnnamedTable(Tools=tools, ActiveTool=self.active_tool.name)

    def __repr__(self) -> str:
        return repr(self.render())

    def add_tool(self, id: str, name: str, position: tuple[int, int] = (0, 0)) -> Tool:
        new_tool = Tool(id, name, position)

        self.add_tools(new_tool)

        return new_tool

    def add_tools(self, *tools) -> Composition:
        if not tools:
            return self

        for tool in tools:
            self.add_tool(tool)

        return self

    def add_merge(
        self,
        name: str,
        background: Tool | Macro | None,
        foreground: Tool | Macro | None,
        position: tuple[float, float],
    ) -> Tool:
        merge = Tool("Merge", name, position)

        match background:
            case Tool():
                bg_output = background.output
            case Macro():
                bg_output = background.outputs[0].name
            case _:
                bg_output = None
        if bg_output:
            bg_input = Input(
                "Background", source_operator=background.name, source=bg_output
            )

        match foreground:
            case Tool():
                fg_output = foreground.output
            case Macro():
                fg_output = foreground.outputs[0].name
            case _:
                fg_output = None
        if fg_output:
            fg_input = Input(
                "Foreground", source_operator=foreground.name, source=fg_output
            )

        merge.add_inputs(bg_input, fg_input)

        return merge


class Operator(Protocol):
    @property
    def name(self) -> str:
        ...

    def render(self) -> NamedTable | UnnamedTable:
        ...
