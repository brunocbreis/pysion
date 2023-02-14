from dataclasses import dataclass


@dataclass
class RGBA:
    """Defines an RGB + Alpha color using 0 to 1 floats. Defaults to fully opaque black."""

    red: float = 0
    green: float = 0
    blue: float = 0
    alpha: float = 1
    premultiply: bool = True

    def __post_init__(self):
        if self.premultiply:
            self.red *= self.alpha
            self.green *= self.alpha
            self.blue *= self.alpha
