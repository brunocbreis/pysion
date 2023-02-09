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
