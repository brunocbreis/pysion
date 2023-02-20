from pysion import Tool, Composition, Input, Macro, RGBA, FuID


def main():
    comp = Composition()
    tool = (
        Tool("sRectangle", "Rect")
        .add_color_input(RGBA(0.2, 0.3, 0.4))
        .add_inputs(Width=0.6, Filter=FuID("Multi-box"))
        .add_input(Input("Height", 0.3, expression="Width / 2"))
    )
    render = (
        Tool("sRender", "Render", (1, 0))
        .add_source_input("Input", source_operator=tool.name, source=tool.output)
        .add_inputs(Width=1920, Height=1080)
    )

    macro = (
        Macro("Ball", tile_color=RGBA(0.5, 1, 1))
        .add_tools(tool, render)
        .add_input(tool, "Width", "Cool Width")
    )

    comp.add_tools(macro)

    print(comp)

    srect = (
        Tool("sRectangle", f"GeomColShape1")
        .add_inputs(
            Width=1920,
            Height=1080,
            Red=1,
            Green=0.5,
            Blue=0.5,
            Alpha=1,
        )
        .add_inputs(**{'["Translate.X"]': -0.2})
    )

    print(srect)


def main2():
    comp = Composition()

    bg = Tool.background(
        "Background1", RGBA(1, 0.4, 0.1), resolution="auto", position=(0, 0)
    )
    mask = Tool.mask("Rectangle", type="Rectangle", position=(0, -1))
    bg.add_mask(mask)

    comp.add_tools(bg, mask)

    print(comp.render())


if __name__ == "__main__":
    main2()
