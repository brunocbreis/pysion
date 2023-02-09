from .utils import fusion_coords, fusion_point


def generate_tool(
    tool_id: str, tool_name: str, inputs: str = "", position: tuple[int, int] = (0, 0)
) -> str:
    """Creates a Fusion tool"""
    x, y = fusion_coords(position)
    tool = (
        f"\t\t{tool_name} = {tool_id} {{\n\t\t\tInputs = {{\t\t\t\t{inputs}\n\t\t\t}},"
        f"\n\t\t\tViewInfo = OperatorInfo {{ Pos = {fusion_point(x,y)} }},\n\t\t}},\n"
    )
    return tool


def generate_inputs(**inputs: dict[str, float | int | str]) -> str:
    """Creates strings for adding inputs to Fusion tools"""

    result = ""
    for key, value in inputs.items():
        result += f"\n\t\t\t\t{key} = Input {{ Value = {value}, }},"

    return result


def generate_source_input(
    input: str, tool_name: str, tool_output: str = "Output"
) -> str:
    """
    Creates string for tools that get Inputs from other tools,
    e.g from a Mask or to a Merge
    """

    result = (
        f'\n\t\t\t\t{input} = Input {{\n\t\t\t\t\tSourceOp = "{tool_name}",'
        f'\n\t\t\t\t\tSource = "{tool_output}",\n\t\t\t\t}},'
    )
    return result


def generate_mask(mask_name: str) -> str:
    return generate_source_input("EffectMask", mask_name, "Mask")


def generate_instance_input(
    instance_name: str,
    source_op: str,
    source_input: str,
    default: str | int | float = "",
    **inputs,
) -> str:
    if default:
        if type(default) is str:
            default = f'\n\t\t\t\t\tDefault = "{default}",'
        else:
            default = f"\n\t\t\t\t\tDefault = {default},"

    if inputs:
        inps = "".join(
            [
                f'\n\t\t\t\t\t{k} = "{v}",'
                if type(v) is str
                else f"\n\t\t\t\t\t{k} = {v},"
                for (k, v) in inputs.items()
            ]
        )

    else:
        inps = ""

    return (
        f'\n\t\t\t\t{instance_name} = InstanceInput {{\n\t\t\t\t\tSourceOp = "{source_op}",'
        f'\n\t\t\t\t\tSource = "{source_input}",{default}{inps}\n\t\t\t\t}},'
    )


def generate_instance_output(
    source_op: str, source_input: str = "Output", instance_name: str = "Output"
) -> str:
    return (
        f'\n\t\t\t\t{instance_name} = InstanceOutput {{\n\t\t\t\t\tSourceOp = "{source_op}",'
        f'\n\t\t\t\t\tSource = "{source_input}",\n\t\t\t\t}},'
    )


def generate_published_polyline(
    points: list[tuple[float, float]], point_name: str = "Point"
) -> str:
    head = (
        "\n\t\t\t\tPolyline = Input {"
        "\n\t\t\t\t\tValue = Polyline {"
        "\n\t\t\t\t\t\tPoints = {"
    )
    joint = "\n\t\t\t\t\t\t}\n\t\t\t\t\t},\n\t\t\t\t},"

    point_ids = "".join([_point_id(i, point_name) for i, _ in enumerate(points)])

    point_data = "".join(
        generate_inputs(
            **{
                f"{point_name}{i}": fusion_point(p[0], p[1])
                for i, p in enumerate(points)
            }
        )
    )

    return head + point_ids + joint + point_data


def _point_id(index: int, name: str = "Point") -> str:
    return f'\n\t\t\t\t\t\t\t{{ PublishID = "{name}{index}" }},'
