from pysion import Tool, Composition
from pysion.values import ToolID
from pathlib import Path

# Set up path for saving and retrieving expected results
FOLDER = Path("tests") / "expected_results" / "tool"


def compare_result(name: str, result: Composition) -> str:
    file_name = f"{name}.setting"

    with open(FOLDER / file_name, "r") as file:
        xp_result = file.read()

    assert repr(result) == xp_result


def test_add_mask():
    blur = Tool(ToolID.blur, "Blur")
    mask = Tool.mask("Mask", "BSpline", (-1, 0))
    blur.add_mask(mask)

    comp = Composition(blur, mask)

    comp.copy()

    compare_result("test_add_mask", comp)


def test_offset_position():
    blur = Tool(ToolID.blur, "Blur")
    blur.offset_position((1, 1))

    assert blur.position == (1, 1)


def test_instance():
    blur = Tool(ToolID.blur, "Blur")
    blur_instance = blur.add_instance()

    assert blur.name == blur_instance.source_op == "Blur"
