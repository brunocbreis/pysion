def fusion_coords(coords: tuple[int, int]) -> tuple[int, int]:
    """Converts x, y coords into Fusion flow scale"""
    x, y = coords
    return x * 110, y * 33
