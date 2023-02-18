from __future__ import annotations
from dataclasses import dataclass
from .named_table import NamedTable, UnnamedTable
from .tool import Tool
from .macro import Macro
from typing import Protocol
from .input import Input
from .animation import BezierSpline, Curve


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
        if not self.active_tool:
            if self.tools:
                self.active_tool = self.tools[-1]

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

        if not self.tools:
            self.tools: list[Operator] = []

        for tool in tools:
            if isinstance(tool, Tool):
                self.tools.append(tool)

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

    def animate(self, tool: Tool | str, input_name: str) -> BezierSpline:
        match tool:
            case Tool():
                # TODO: test if tool is in comp
                tool_name = tool.name
            case str():
                try:
                    tool = self.tools[tool]
                    tool_name = tool
                except KeyError:
                    raise ValueError(f"{tool} is not one of the tools in this comp.")
            case _:
                raise ValueError("Please add a valid Tool or Tool name.")

        new_spline = BezierSpline(f"{tool_name}{input_name}")

        tool.add_source_input(input_name, new_spline.name, "Value")
        self.tools.append(new_spline)

        return new_spline


class Operator(Protocol):
    @property
    def name(self) -> str:
        ...

    def render(self) -> NamedTable | UnnamedTable:
        ...
