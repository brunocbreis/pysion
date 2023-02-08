from .generators import add_tool, add_inputs, add_source_input
from dataclasses import dataclass


@dataclass
class Tool:
    id: str
    name: str
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self._inputs: dict[str, int | float | str] = {}
        self._source_inputs: dict[str, tuple[str, str]] = {}
        self.mask = ""

    def __str__(self) -> str:
        source_inputs = ""
        if self.source_inputs:
            for k, v in self.source_inputs.items():
                source_inputs += add_source_input(k, v[0], v[1])

        return add_tool(
            self.id, self.name, add_inputs(**self.inputs) + source_inputs, self.position
        )

    @property
    def inputs(self):
        return self._inputs

    def add_inputs(self, **kwargs):
        for k, v in kwargs.items():
            self._inputs[k] = v

    @property
    def source_inputs(self):
        return self._source_inputs

    def add_source_input(self, input: str, tool_name: str, tool_output: str) -> None:
        self._source_inputs[input] = (tool_name, tool_output)

    def add_mask(self, mask_name: str):
        self.add_source_input("EffectMask", mask_name, "Mask")
