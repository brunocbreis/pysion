from dataclasses import dataclass
from types import SimpleNamespace


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


class TileColor(SimpleNamespace):
    """Shortcut for acceptable tile colors in DaVinci Resolve / Fusion"""

    orange = RGBA(0.92156862745098, 0.431372549019608, 0)
    apricot = RGBA(1, 0.658823529411765, 0.2)
    yellow = RGBA(0.886274509803922, 0.662745098039216, 0.109803921568627)
    lime = RGBA(0.623529411764706, 0.776470588235294, 0.0823529411764706)
    olive = RGBA(0.372549019607843, 0.6, 0.125490196078431)
    green = RGBA(0.250980392156863, 0.56078431372549, 0.396078431372549)
    teal = RGBA(0, 0.596078431372549, 0.6)
    navy = RGBA(0.0823529411764706, 0.384313725490196, 0.517647058823529)
    blue = RGBA(0.474509803921569, 0.658823529411765, 0.815686274509804)
    purple = RGBA(0.6, 0.450980392156863, 0.627450980392157)
    violet = RGBA(0.584313725490196, 0.294117647058824, 0.803921568627451)
    pink = RGBA(0.913725490196078, 0.549019607843137, 0.709803921568627)
    tan = RGBA(0.725490196078431, 0.690196078431373, 0.592156862745098)
    beige = RGBA(0.776470588235294, 0.627450980392157, 0.466666666666667)
    brown = RGBA(0.6, 0.4, 0)
    chocolate = RGBA(0.549019607843137, 0.352941176470588, 0.247058823529412)
