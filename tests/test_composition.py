from pysion import Composition, RGBA, ToolID, Tool, Macro
from pysion.animation import Curve
from pathlib import Path
import pytest


# Set up path for saving and retrieving expected results
FOLDER = Path("tests") / "expected_results" / "composition"


def expected_result(name: str) -> str:
    file_name = f"{name}.setting"

    with open(FOLDER / file_name, "r") as file:
        return file.read()


# Base comp fixture for testing
@pytest.fixture
def comp() -> Composition:
    comp = Composition()
    comp.add_tool("Background", "MyBackground")
    comp.add_tool("Blur", "MyBlur", (1, 0))
    comp.add_tool("Transform", "MyXF", (2, 0))

    return comp


# Actual tests
def test_base_test_comp(comp: Composition):
    assert repr(comp) == expected_result("base_test_comp")


def test_add_merge(comp: Composition):
    comp.add_merge("Merge1", comp["MyBackground"], comp["MyBlur"], (1, 1))

    print(comp)
    assert repr(comp) == expected_result("test_add_merge")


def test_add_text(comp: Composition):
    comp.add_text(
        "Text1",
        "Testing Text",
        font_face="Arial",
        font_style="Italic",
        color=RGBA(0.3, 0.7, 1),
        position=(0, -1),
    )

    assert repr(comp) == expected_result("test_add_text")


def test_animate(comp: Composition):
    blur_spline = comp.animate("MyBlur", "Blur", default_curve=Curve.linear())
    blur_spline.add_keyframes([(0, 0), (24, 20)], curve=Curve.ease_in_and_out())
    blur_spline[12] = 15

    xf = comp["MyXF"]
    size_spline = comp.animate(xf, "Size", keyframes=[(0, 0), (12, 2)])
    size_spline.apply_curve(Curve.ease_in())

    assert repr(comp) == expected_result("test_animate")


def test_animate_position(comp: Composition):
    pos = comp.animate_position("MyXF", default_curve_x=Curve.decelerate_in_and_out())

    pos[0] = (0.5, 0.5)
    pos[12] = (None, 0.8)
    pos[24] = (0.25, 0.5)

    comp.animate_position(
        comp["MyXF"],
        "Pivot",
        default_curve_x=Curve.decelerate_in(),
        default_curve_y=Curve.ease_out(),
        keyframes=[(0, (0.3, 0.4)), (24, (0.2, 0.5))],
    )

    assert repr(comp) == expected_result("test_animate_position")


def test_auto_name_tool():
    comp = Composition()
    bg1 = comp.add_tool(ToolID.BACKGROUND)
    bg2 = comp.add_tool("Background")

    assert bg1.name == "Background1"
    assert bg2.name == "Background2"


def test_publish(comp: Composition):
    comp.publish(comp["MyBackground"], "TopLeftRed", 1)

    comp.copy()


def test_merge_macro(comp: Composition):
    new_tools = (Tool(ToolID.BACKGROUND, "NewBG"), Tool(ToolID.BLUR, "NewBlur"))
    macro = Macro("MyMacro").add_tools(*new_tools)

    comp.add_merge("MergeMacro", macro, comp["MyBackground"])

    assert comp["MergeMacro"]["Background"].source_operator == macro.name
