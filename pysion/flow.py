def fusion_coords(coords: tuple[int, int]) -> tuple[int, int]:
    """Converts x, y coords into Fusion flow scale"""
    x, y = coords
    return x * 110, y * 33


def offset_position(
    coords: tuple[int, int], offset: tuple[int, int]
) -> tuple[int, int]:
    return (coords[0] + offset[0], coords[1] + offset[1])
