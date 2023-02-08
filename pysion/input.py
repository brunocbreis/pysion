from dataclasses import dataclass
from .generators import generate_inputs, generate_instance_input, generate_source_input


@dataclass
class Input:
    parent: str
    name: str
    value: int | float | str
    default: int | float | str = ""

    def __post_init__(self):
        self._instance_properties: dict[str, int | float | str] = {}

    @property
    def instance_properties(self) -> dict[str, int | float | str]:
        return self._instance_properties

    @instance_properties.setter
    def instance_properties(self, **values):
        for k, v in values.items():
            self._instance_properties[k] = v

    @property
    def string(self) -> str:
        return generate_inputs(**{self.name: self.value})

    @property
    def instance(self) -> str:
        return generate_instance_input(
            f"{self.name}Instance",
            self.parent,
            self.name,
            self.default,
            **self.instance_properties,
        )


@dataclass
class SourceInput:
    parent: str
    name: str
    source_operator: str
    source_output: str = "Output"

    @property
    def string(self) -> str:
        return generate_source_input(
            self.name, self.source_operator, self.source_output
        )


@dataclass
class MaskInput(SourceInput):
    parent: str
    source_operator: str

    def __post_init__(self):
        self.source_output: str = "Mask"
        self.name: str = "EffectMask"

    @property
    def string(self) -> str:
        return super().string
