from __future__ import annotations
from .tool import Tool
from dataclasses import dataclass
from .input import Input
from .named_table import UnnamedTable, NamedTable
from typing import Literal
from .flow import fusion_coords
from .color import RGBA


@dataclass
class Macro:
    """Represents a Fusion Macro. Outputs a NamedTable, with the Macro ID being the name."""

    name: str
    type: Literal["macro", "group"] = "macro"
    inputs: UnnamedTable | None = None  # [str, InstanceInput]
    tools: UnnamedTable[str, Tool] | None = None  # [str, Tool]
    position: tuple[int, int] = (0, 0)
    tile_color: RGBA | None = None

    def __post_init__(self):
        self.id = self.type.capitalize() + "Operator"
        self._outputs: list[InstanceOutput] = None

    def render(self) -> NamedTable:

        outputs: UnnamedTable[str, NamedTable] = UnnamedTable(
            {output.name: output.nt for output in self.outputs}
        )

        inputs = None
        if self.inputs:
            inputs: UnnamedTable[str, NamedTable] = UnnamedTable(
                {k: v.nt for k, v in self.inputs.items()}
            )

        tools: UnnamedTable[str, NamedTable] = UnnamedTable(
            {tool.name: tool.render() for tool in self.tools.values()},
            force_indent=True,
        )

        return NamedTable(
            self.id,
            Inputs=inputs,
            Outputs=outputs,
            Tools=tools,
            ViewInfo=self.position_nt,
            Colors=self.color_nt,
            force_indent=True,
        )

    def __repr__(self) -> str:
        return repr(self.render())

    def _render_position(self) -> NamedTable:
        return NamedTable("GroupInfo", Pos=fusion_coords(self.position))

    def _render_color(self) -> UnnamedTable | None:
        if not self.tile_color:
            return None

        tile_color = UnnamedTable(
            R=self.tile_color.red,
            G=self.tile_color.green,
            B=self.tile_color.blue,
            force_unindent=True,
        )

        return UnnamedTable(TileColor=tile_color)

    @property
    def outputs(self) -> list[InstanceOutput]:
        if self._outputs:
            return self._outputs

        if self._outputs is None:
            self._outputs: list[InstanceOutput] = []
            if not self.tools:
                raise ValueError(
                    "Macro has no tools yet. Please add a tool so it can have outputs."
                )

        last_tool = list(self.tools.values())[-1]
        self.add_output(last_tool)

        return self._outputs

    @property
    def color_nt(self) -> NamedTable:
        return self._render_color()

    @property
    def position_nt(self) -> NamedTable:
        return self._render_position()

    def add_input(
        self,
        tool: Tool,
        input_name: str,
        pretty_name: str | None = None,
        page: str | None = None,
        control_group: int | None = None,
    ) -> Macro:
        if self.inputs is None:
            self.inputs = UnnamedTable(force_indent=True)

        try:
            input: Input = tool.inputs[input_name]
            default_value = input.value
        except KeyError:
            default_value = None

        if pretty_name is None:
            pretty_name = input_name

        new_instance = InstanceInput(
            pretty_name=pretty_name,
            fusion_name=f"{input_name}Instance",
            source_operator=tool.name,
            source=input_name,
            default=default_value,
            page=page,
            control_group=control_group,
        )

        self.inputs[new_instance.proper_name] = new_instance

        return self

    def add_output(self, tool: Tool) -> Macro:
        if self._outputs is None:
            self._outputs: list[InstanceOutput] = []

        name = f"Output{len(self._outputs)+1}"

        new_output = InstanceOutput(name, tool.name, tool.output)

        self._outputs.append(new_output)

        return self

    def add_color_input(
        self,
        tool: Tool,
        name: str = "Color",
        group: int = 1,
        prefix: str = "TopLeft",
        suffix: str = "",
    ):
        """Adds all necessary color inputs as the same control group. If adding more than one, group should be incremented.
        Different Prefixes and Suffixes are added to color inputs in Fusion. Backgrounds usually default to TopLeft[Color]
        for solid fills. Text+ nodes have [Color]1, [Color]2 etc for different layers.
        """

        self.add_input(
            tool=tool,
            input_name=f"{prefix}Red{suffix}",
            pretty_name=name,
            control_group=group,
        ).add_input(
            tool=tool,
            input_name=f"{prefix}Green{suffix}",
            control_group=group,
        ).add_input(
            tool=tool,
            input_name=f"{prefix}Blue{suffix}",
            control_group=group,
        ).add_input(
            tool=tool,
            input_name=f"{prefix}Alpha{suffix}",
            control_group=group,
        )

        return self

    def add_tool(self, tool: Tool) -> Macro:
        if self.tools is None:
            self.tools = UnnamedTable()

        self.tools[tool.name] = tool

        return self

    def add_tools(self, *tools) -> Macro:
        if not tools:
            return self
        for tool in tools:
            self.add_tool(tool)

        return self


@dataclass
class InstanceInput:
    """Represents a Fusion InstanceInput. Outputs a NamedTable."""

    pretty_name: str
    source_operator: str
    source: str
    default: int | float | str | list[float] | NamedTable | None = None
    page: str | None = None
    control_group: int | None = None
    fusion_name: str | None = None

    @property
    def nt(self) -> NamedTable:
        return NamedTable(
            "InstanceInput",
            Name=self.pretty_name,
            SourceOp=self.source_operator,
            Source=self.source,
            Default=self.default,
            Page=self.page,
            ControlGroup=self.control_group,
            force_indent=True,
        )

    @property
    def proper_name(self) -> str:
        """Returns a proper name for the input, without spaces."""
        if self.fusion_name:
            return self.fusion_name
        return self.pretty_name.replace(" ", "")

    def __repr__(self) -> str:
        return repr(self.nt)


@dataclass
class InstanceOutput:
    """Represents a Fusion InstanceOutput. Outputs a NamedTable."""

    name: str
    source_operator: str
    source: str

    @property
    def nt(self) -> NamedTable:
        return NamedTable(
            "InstanceOutput",
            SourceOp=self.source_operator,
            Source=self.source,
            force_indent=True,
        )

    def __repr__(self) -> str:
        return repr(self.nt)
