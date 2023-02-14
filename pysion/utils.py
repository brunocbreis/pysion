def fusion_coords(coords: tuple[int, int]) -> tuple[int, int]:
    """Converts x, y coords into Fusion flow scale"""
    x, y = coords
    return x * 110, y * 33


# animation still undeveloped
def kf_pairs(keyframes: list[int]) -> zip:
    return zip(keyframes, keyframes[1:])


# about to deprecate
def fu_id(name: str) -> str:
    return f'FuID {{ "{name}" }}'
