from types import SimpleNamespace


class ToolID(SimpleNamespace):
    # Media
    media_in = "MediaIn"
    media_out = "MediaOut"
    loader = "Loader"
    saver = "Saver"

    # Generators
    background = "Background"
    text = "TextPlus"
    fast_noise = "FastNoise"
    paint = "Paint"

    # Effects
    color_corrector = "ColorCorrector"
    cc = "ColorCorrector"
    color_curves = "ColorCurves"
    curves = "ColorCurves"
    brightness_contrast = "BrightnessContrast"
    bc = "BrightnessContrast"
    blur = "Blur"

    # Transform and composite
    transform = "Transform"
    xf = "Transform"
    merge = "Merge"
    mrg = "Merge"
    dissolve = "Dissolve"
    dx = "Dissolve"
    channel_booleans = "ChannelBooleans"
    matte_control = "MatteControl"

    # Shape nodes
    s_rectangle = "sRectangle"
    s_ellipse = "sEllipse"
    s_ngon = "sNGon"
    s_render = "sRender"
    s_merge = "sMerge"
    s_transform = "sTransform"
    s_duplicate = "sDuplicate"
    s_boolean = "sBoolean"
    s_outline = "sOutline"
