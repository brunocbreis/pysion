from __future__ import annotations
from dataclasses import dataclass
from .named_table import UnnamedTable
from enum import Enum
from typing import Literal


class UC_dtype(Enum):
    NUMBER = "Number"
    POINT = "Point"
    TEXT = "Text"


class UC_input_control(Enum):
    SLIDER = "SliderControl"
    COMBO = "ComboControl"
    SCREW = "ScrewControl"


@dataclass
class UserControl:
    pretty_name: str
    input_control: str | Literal = UC_input_control.SLIDER
    data_type: str | Literal = UC_dtype.NUMBER
    is_integer: bool | None = False
    page: str | None = None
    default: int | float | str | None = None
    min_scale: int | float | None = None
    max_scale: int | float | None = None
    min_allowed: int | float | None = None
    max_allowed: int | float | None = None

    def __post_init__(self):
        self.name = self.pretty_name.replace(" ", "")

    def __repr__(self) -> str:
        return repr(self.render())

    def render(self) -> UnnamedTable:
        return UnnamedTable(
            LINKS_Name=self.pretty_name,
            LINKID_DataType=self.data_type,
            INPID_InputControl=self.input_control,
            INP_Integer=self.is_integer,
            ICS_ControlPage=self.page,
            INP_MinScale=self.min_scale,
            INP_MaxScale=self.max_scale,
            INP_MinAllowed=self.min_allowed,
            INP_MaxAllowed=self.max_allowed,
            INP_Default=self.default,
        )
