from dataclasses import dataclass


def fusion_coords(coords: tuple[int, int]) -> tuple[int, int]:
    """Converts x, y coords into Fusion flow scale"""
    x, y = coords
    return x * 110, y * 33


def fusion_point(x: float, y: float) -> str:
    return f"{{ {x}, {y} }}"


def kf_pairs(keyframes: list[int]) -> zip:
    return zip(keyframes, keyframes[1:])


def fusion_string(string: str) -> str:
    """Returns a string with added quotes"""
    return f'"{string}"'


@dataclass
class RGBA:
    """Defines an RGB + Alpha color using 0 to 1 floats. Defaults to fully opaque black."""

    red: float = 0
    green: float = 0
    blue: float = 0
    alpha: float = 1
    premultiply = True

    def __post_init__(self):
        if self.premultiply:
            self.red *= self.alpha
            self.green *= self.alpha
            self.blue *= self.alpha
