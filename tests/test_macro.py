from pysion import Composition, Macro, Tool, RGBA
from pysion.color import TileColor
from pathlib import Path
import pytest


# Set up path for saving and retrieving expected results
FOLDER = Path("tests") / "expected_results" / "macro"


def compare_result(name: str, result: Composition) -> str:
    file_name = f"{name}.setting"

    with open(FOLDER / file_name, "r") as file:
        xp_result = file.read()

    assert repr(result) == xp_result


# Base comp fixture for testing
@pytest.fixture
def base_test_tools() -> tuple[Tool, Tool, Tool]:

    bg = Tool.background("TestBG", RGBA(1, 1, 0.2, premultiply=False))
    title = Tool.text("TestTXT", "Hello world!", position=(1, -1), color=RGBA())
    merge = Tool.merge("TestMerge", bg, title, (1, 0))

    return bg, title, merge


@pytest.fixture
def base_test_macro(base_test_tools) -> Macro:
    return Macro("TestMacro").add_tools(*base_test_tools)


# Actual tests
def test_base_test_comp(base_test_tools):
    compare_result("base_test_comp", Composition(*base_test_tools))


def test_create_macro(base_test_tools: tuple[Tool, Tool, Tool]):
    bg, title, merge = base_test_tools

    macro = Macro("TestMacro")
    macro.add_tools(bg, title)
    macro.add_tool(merge)

    comp = Composition(macro)

    compare_result("test_create_macro", comp)


def test_color_input(base_test_macro: Macro):
    base_test_macro.add_color_input(base_test_macro.tools["TestBG"])

    comp = Composition(base_test_macro)

    compare_result("test_color_input", comp)


def test_add_input(base_test_macro: Macro, base_test_tools: tuple[Tool, Tool, Tool]):
    base_test_macro.add_input(base_test_tools[1], "Size")

    comp = Composition(base_test_macro)

    compare_result("test_add_input", comp)


def test_tile_color(base_test_macro: Macro):
    base_test_macro.tile_color = TileColor.lime

    comp = Composition(base_test_macro)

    compare_result("test_tile_color", comp)
