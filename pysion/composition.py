from __future__ import annotations
from dataclasses import dataclass
from .named_table import NamedTable, UnnamedTable
from .tool import Tool
from typing import Protocol


class Operator(Protocol):
    @property
    def name(self) -> str:
        ...

    def render(self) -> NamedTable | UnnamedTable:
        ...


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
        ut = UnnamedTable(
            {tool.name: tool.render() for tool in self.tools}, force_indent=True
        )

        return UnnamedTable(Tools=ut, ActiveTool=self.active_tool.name)

    def __repr__(self) -> str:
        return repr(self.render())

    def add_tool(self, tool: Tool) -> Composition:
        if self.tools is None:
            self.tools: list[Operator] = []

        self.tools.append(tool)

        if not self.active_tool:
            self.active_tool = tool

        return self

    def add_tools(self, *tools) -> Composition:
        if not tools:
            return self

        for tool in tools:
            self.add_tool(tool)

        return self
