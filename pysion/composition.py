from __future__ import annotations
from .named_table import NamedTable, UnnamedTable
from .tool import Tool
from .modifier import Modifier
from .macro import Macro
from typing import Protocol
from .input import Input
from .animation import BezierSpline, Curve
from .named_table import FuID

try:
    from pyperclip import copy

    PYPERCLIP_INSTALLED = True
except ImportError:
    PYPERCLIP_INSTALLED = False


class Operator(Protocol):
    @property
    def name(self) -> str:
        ...

    def render(self) -> NamedTable | UnnamedTable:
        ...


class Composition:
    """Represents a Fusion composition. Outputs an UnnamedTable with tool names as keys and tools as NamedTables."""

    def __init__(self, *tools: Tool | Macro) -> None:
        self.tools: UnnamedTable[str, Tool | Macro] = None
        self._last_added_tool: Tool = None

        if tools:
            self.add_tools(*tools)

        self.active_tool_name: str | None = None
        self.modifiers: UnnamedTable[str, Operator] | None = None

    def render(self) -> UnnamedTable:
        self._auto_set_active_tool()

        operators = self._render_operators()

        if not operators:
            print("Comp is empty.")
            return None

        return UnnamedTable(Tools=operators, ActiveTool=self.active_tool_name)

    def copy(self) -> None:
        if PYPERCLIP_INSTALLED:
            return copy(repr(self))

        print(
            "For comp.copy() support, make sure to install optional dependency pyperclip."
        )

    def __repr__(self) -> str:
        return repr(self.render())

    def __getitem__(self, key: str) -> Operator:
        assert isinstance(key, str)

        if self.tools is None and self.modifiers is None:
            raise KeyError

        if self.modifiers is None:
            return self.tools[key]
        else:
            return self.modifiers[key]

    def __setitem__(self, key: str, value: Tool | Macro):
        assert isinstance(key, str)
        assert isinstance(value, Tool | Macro)

        self.add_tools(value)

    # Private methods
    def _auto_set_active_tool(self) -> None:
        if not self.tools:
            self.active_tool_name = None
            return

        if not self.active_tool_name:
            self.active_tool_name = self._last_added_tool.name

    def _render_operators(self) -> UnnamedTable:
        operators = UnnamedTable(force_indent=True)

        if self.tools:
            operators.update(
                {tool_name: tool.render() for tool_name, tool in self.tools.items()}
            )
        if self.modifiers:
            operators.update(
                {mod_name: mod.render() for mod_name, mod in self.modifiers.items()}
            )

        return operators

    def _add_tool(self, tool: Tool | Macro) -> Operator:
        if self.tools is None:
            self.tools: UnnamedTable[str, Tool | Macro] = UnnamedTable()

        self.tools[tool.name] = tool
        self._last_added_tool = tool

        return tool

    def _add_modifier(self, modifier: Operator) -> Operator:
        if self.modifiers is None:
            self.modifiers: UnnamedTable[str, Operator] = UnnamedTable()

        self.modifiers[modifier.name] = modifier

        return modifier

    # Public methods
    # Tools
    def add_tool(self, id: str, name: str, position: tuple[int, int] = (0, 0)) -> Tool:
        new_tool = Tool(id, name, position)

        return self._add_tool(new_tool)

    def add_tools(self, *tools: Operator) -> Composition:
        if not tools:
            return self

        for tool in tools:
            self._add_tool(tool)

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

    # Modifiers
    def animate(
        self, tool: Tool | str, input_name: str, default_curve: Curve | None = None
    ) -> BezierSpline:
        match tool:
            case Tool():
                if tool not in self.tools.values():
                    print(f"Adding {tool.name} to the comp.")
                    self.add_tools(tool)

                tool_name = tool.name
            case str():
                try:
                    tool_name = tool
                    tool = self[tool]
                except KeyError:
                    raise ValueError(f"{tool} is not one of the tools in this comp.")
            case _:
                raise ValueError("Please add a valid Tool or Tool name.")

        new_spline = BezierSpline(f"{tool_name}{input_name}", default_curve)

        tool.add_source_input(input_name, new_spline.name, "Value")
        tool[input_name].spline = new_spline

        return self._add_modifier(new_spline)

    def publish(
        self,
        tool: Tool,
        input: str,
        value: int | float | tuple[int | float, int | float] | str | FuID,
    ) -> Modifier:

        id = "Publish"
        match value:
            case int() | float():
                id += "Number"
            case str():
                id += "Text"
            case tuple():
                id += "Point"
            case FuID():
                id += "FuID"
            case _:
                raise ValueError

        name = f"Publish{tool.name}{input}"

        new_published_value = Modifier(id, name)
        new_published_value.add_inputs(Value=value)

        tool.add_source_input(input, name, "Value")

        return self._add_modifier(new_published_value)

    def connect(
        self,
        tool_out: Tool,
        tool_in: Tool,
        source_out: str = "Output",
        source_in: str = "Input",
    ) -> Composition:
        tool_in.add_source_input(source_in, tool_out.name, source_out)

        return self

    def connect_to_published_value(
        self, published_value: Tool, tool_in: Tool, source_in: str
    ) -> Composition:
        return self.connect(published_value, tool_in, "Value", source_in)
