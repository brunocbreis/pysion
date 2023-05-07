import pysion
from pysion.color import RGBA
from pysion.animation import Curve

# We always start by initializing a new comp
comp = pysion.Composition()

# Creating a Text+ node using a shortcut method
title = comp.add_text(
    name="MyTitle",
    text="This is my title",
    # font_face="Forma DJR Display",
    # ^ this is what's shown in the gif, but the line below works everywhere:
    font_face="Open Sans",
    color=RGBA(red=0.15, green=0.2, blue=0.9),
)

# You can add inputs by assignment:
title["Size"] = 0.2

# Animating position with some keyframes
title_pos = comp.animate_position(title, default_curve_x=Curve.ease_in(strength=0.75))
title_pos[0] = (-0.5, 0.5)
title_pos[24] = (0.5, None)

# Creating a background using pysion.Tool method
bg = pysion.Tool.background("OrangeBG", RGBA(1, 0.4, 0.1), position=(-1, 1))

# Merging it over the text
mrg = pysion.Tool.merge("MergeTitle", bg, title, position=(0, 1))

# And adding the manually created tools to the comp
comp.add_tools(bg, mrg)

# Let's add a MediaOut node for use in Resolve
media_out = comp.add_tool("MediaOut", position=(1, 1))
comp.connect(mrg, media_out)

# The line below is an alternative that adds the tools and creates the merge in one go:
# comp.add_merge("MergeTitle", bg, title, position=(0, 1))

# Copying the comp code to the clipboard
comp.copy()
