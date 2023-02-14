from __future__ import annotations
from .tool import Tool
from dataclasses import dataclass
from .input import Input
from .named_table import UnnamedTable, NamedTable
from typing import Literal
from .flow import fusion_coords
from .rgba import RGBA


@dataclass
class Macro:
    """Represents a Fusion Macro. Outputs a NamedTable, with the Macro ID being the name."""

    name: str
    type: Literal["macro", "group"] = "macro"
    inputs: UnnamedTable | None = None  # [str, InstanceInput]
    tools: UnnamedTable | None = None  # [str, Tool]
    position: tuple[int, int] = (0, 0)
    outputs: UnnamedTable = None  # [str, InstanceOutput]
    tile_color: RGBA | None = None

    def __post_init__(self):
        self.id = self.type.capitalize() + "Operator"

    def render(self) -> NamedTable:
        if not self.outputs:
            if self.tools:
                last_tool: Tool = list(self.tools.values())[-1]

                print(
                    f"Warning: adding last added tool ({last_tool.name}) output as macro output."
                )
                self.add_output("Output", last_tool)

        return NamedTable(
            self.id,
            Inputs=self.inputs,
            Outputs=self.outputs,
            Tools=self.tools,
            ViewInfo=self.position_nt,
            Colors=self.color_nt,
            force_indent=True,
        )

    def __repr__(self) -> str:
        return repr(self.render())

    def _render_position(self) -> NamedTable:
        return NamedTable("GroupInfo", Pos=fusion_coords(self.position))

    def _render_color(self) -> UnnamedTable:
        tile_color = UnnamedTable(
            R=self.tile_color.red,
            G=self.tile_color.green,
            B=self.tile_color.blue,
            force_unindent=True,
        )

        return UnnamedTable(TileColor=tile_color)

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
        except KeyError:
            raise ValueError(
                f"Please add a valid input name. Are you sure {input_name} is one of {tool.name}'s inputs?"
            )

        if pretty_name is None:
            pretty_name = input.name

        new_instance = InstanceInput(
            name=pretty_name,
            source_operator=tool.name,
            source=input_name,
            default=input.value,
            page=page,
            control_group=control_group,
        )

        self.inputs[new_instance.proper_name] = new_instance

        return self

    def add_output(self, name: str, tool: Tool) -> Macro:
        op = InstanceOutput(name, tool.name, tool.output)

        if self.outputs is None:
            self.outputs = UnnamedTable()

        self.outputs[name] = op

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
            pretty_name=name,
            control_group=group,
        ).add_input(
            tool=tool,
            input_name=f"{prefix}Blue{suffix}",
            pretty_name=name,
            control_group=group,
        ).add_input(
            tool=tool,
            input_name=f"{prefix}Alpha{suffix}",
            pretty_name=name,
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

    name: str
    source_operator: str
    source: str
    default: int | float | str | list[float] | NamedTable | None = None
    page: str | None = None
    control_group: int | None = None

    @property
    def nt(self) -> NamedTable:
        return NamedTable(
            "InstanceInput",
            Name=self.name,
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
        return self.name.replace(" ", "")

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
