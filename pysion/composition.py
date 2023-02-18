from __future__ import annotations
from dataclasses import dataclass
from .named_table import NamedTable, UnnamedTable
from .tool import Tool
from .macro import Macro
from typing import Protocol
from .input import Input
from .animation import BezierSpline


@dataclass
class Composition:
    """Represents a Fusion composition. Outputs an UnnamedTable with tool names as keys and tools as NamedTables."""

    tools: list[Operator] | None = None

    def __post_init__(self) -> None:
        self.active_tool: Tool | None = None
        self.modifiers: list[Operator] | None = None

    def render(self) -> UnnamedTable:
        self._auto_set_active_tool()

        operators = UnnamedTable(force_indent=True)
        if self.tools:
            operators.update({tool.name: tool.render() for tool in self.tools})
        if self.modifiers:
            operators.update(
                {modifier.name: modifier.render() for modifier in self.modifiers}
            )

        if not operators:
            print("Comp is empty.")
            return None

        return UnnamedTable(Tools=operators, ActiveTool=self.active_tool.name)

    def __repr__(self) -> str:
        return repr(self.render())

    def _auto_set_active_tool(self) -> None:
        if not self.active_tool:
            if self.tools:
                self.active_tool = self.tools[-1]

    def add_tool(self, id: str, name: str, position: tuple[int, int] = (0, 0)) -> Tool:
        new_tool = Tool(id, name, position)

        if self.tools is None:
            self.tools: list[Operator] = []

        self.tools.append(new_tool)

        return new_tool

    def add_tools(self, *tools: Operator) -> Composition:
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

        if self.modifiers is None:
            self.modifiers: list[Operator] = []

        self.modifiers.append(new_spline)

        return new_spline

    def publish(self, tool: Tool, input: str) -> Operator:
        ...


class Operator(Protocol):
    @property
    def name(self) -> str:
        ...

    def render(self) -> NamedTable | UnnamedTable:
        ...
