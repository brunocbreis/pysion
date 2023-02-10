from .tool import Tool
from dataclasses import dataclass
from .input import Input, Output
from .wrapper import wrap_for_macro


@dataclass
class Macro:
    name: str
    tools: list[Tool]
    position: tuple[int, int] = (0, 0)
    outputs: list[Output] = None

    def __post_init__(self):
        self.id: str = "MacroOperator"
        self._instanced_inputs: list[Input] = []

        if not self.outputs:
            self._instanced_outputs: list[Output] = [self.tools[-1].outputs[0]]
        else:
            self._instanced_outputs: list[Output] = self.outputs

    @property
    def instanced_inputs(self):
        return self._instanced_inputs

    @property
    def instanced_outputs(self):
        return self._instanced_outputs

    @property
    def string(self):

        instanced_inputs = "".join([ip.instance for ip in self.instanced_inputs])

        instanced_outputs = "".join([op.instance for op in self.instanced_outputs])

        return wrap_for_macro(self, instanced_inputs, instanced_outputs, self.tools)

    def add_instance_input(
        self, input: Input, default: str | int | float = "", **properties
    ):
        new_instance = input
        new_instance.default = default
        new_instance.instance_properties = properties
        self._instanced_inputs.append(new_instance)

        return self

    def add_instance_output(self, tool: Tool):
        self._instanced_outputs += tool.outputs

        return self

    def add_color_input(
        self,
        tool: Tool,
        group: int = 1,
        prefix: str = "TopLeft",
        suffix: str = "",
        **properties,
    ):
        """Adds all necessary color inputs as the same control group. If adding more than one, group should be incremented.
        Different Prefixes and Suffixes are added to color inputs in Fusion. Backgrounds usually default to TopLeft[Color]
        for solid fills. Text+ nodes have [Color]1, [Color]2 etc for different layers.
        """

        self.add_instance_input(
            tool.inputs[f"{prefix}Red{suffix}"],
            ControlGroup=group,
            Name="Color",
            **properties,
        ).add_instance_input(
            tool.inputs[f"{prefix}Green{suffix}"], ControlGroup=group, **properties
        ).add_instance_input(
            tool.inputs[f"{prefix}Blue{suffix}"], ControlGroup=group, **properties
        ).add_instance_input(
            tool.inputs[f"{prefix}Alpha{suffix}"], ControlGroup=group, **properties
        )

        return self

    # Aliases
    add_input = add_instance_input
    add_output = add_instance_output
    add_color = add_color_input
    inputs = instanced_inputs
    outputs = instanced_outputs
