from types import SimpleNamespace


class DType(SimpleNamespace):
    number = "Number"
    point = "Point"
    text = "Text"


class InputControl(SimpleNamespace):
    slider = "SliderControl"
    combo = "ComboControl"
    screw = "ScrewControl"
