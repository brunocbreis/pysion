!["Pysion"](https://github.com/brunocbreis/pysion/blob/master/images/pysion-logo.png)

 ![version: beta](https://img.shields.io/badge/version-beta-blue)   [!["Buy Me A Coffee"](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee)](https://www.buymeacoffee.com/brunoreis)

## A more pythonic way to programmatically create Fusion compositions

**pysion** is a python package / framework for creating Blackmagic [DaVinci Resolve] Fusion comps with code. Comps, tools and inputs are stored in custom python `dict`s that mimic Fusion's `.setting` files lua-like syntax when turned into strings. When you run `comp.render()`, you get text that's readily pasteable into Fusion.

## Example code

It's really easy to create a simple composition with a background and a rectangle mask:

```python
from pysion import Composition, Tool, RGBA

comp = Composition()

bg = Tool.background("Background1", RGBA(1, 0.4, 0.1), resolution="auto")
mask = Tool.mask("Rectangle", position=(0, -1))
bg.add_mask(mask)

comp.add_tools(bg, mask)

print(comp.render())
```

The output...

```lua
{ 
        Tools = { 
                Background1 = Background { 
                        Inputs = { 
                                TopLeftRed = Input { Value = 1, }, 
                                TopLeftGreen = Input { Value = 0.4, }, 
                                TopLeftBlue = Input { Value = 0.1, }, 
                                TopLeftAlpha = Input { Value = 1, }, 
                                UseFrameFormatSettings = Input { Value = 1, }, 
                                EffectMask = Input { 
                                        SourceOp = "Rectangle", 
                                        Source = "Mask", 
                                }, 
                        }, 
                        ViewInfo = OperatorInfo { Pos = { 0, 0 }, }, 
                }, 
                Rectangle = RectangleMask { 
                        ViewInfo = OperatorInfo { Pos = { 0, -33 }, }, 
                }, 
        }, 
        ActiveTool = "Background1", 
}
```

... which results in an orange rectangle when pasted into Fusion:

!["A screenshot of the Blackmagic Fusion UI, with two nodes and the resulting orange rectangle that the code above produced."](https://github.com/brunocbreis/pysion/blob/master/images/example1-screenshot.png)

## How to install

You can install **pysion** by running `pip install git+https://github.com/brunocbreis/pysion` in your terminal of choice.

## What to expect

**pysion** is still very much a work-in-progress, so expect lots of changes and adjustments in its syntax in these beginning stages.

As of right now, I have also been developing [FuPlot](https://github.com/brunocbreis/FuPlot), which relies on **pysion** to generate data visualizations as completely-editable (and animatable) Fusion node trees. I would love to see what else people can come up with!

## To-do

- add user controls
  - add user control pages
- create list of possible FuIDs
- create list of control page icons
- automatically position tools in flow
