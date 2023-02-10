from .tool import Tool
from dataclasses import dataclass
from input import Input, Output
from .wrapper import wrap_for_macro


@dataclass
class Macro:
    name: str
    tools: list[Tool]
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self.id: str = "MacroOperator"
        self._instanced_inputs: list[Input] = []
        self._instanced_outputs: list[Output] = [self.tools[-1].outputs[0]]

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

    def add_instance_output(self, output: Output):
        self._instanced_outputs.append(output)

        return self
