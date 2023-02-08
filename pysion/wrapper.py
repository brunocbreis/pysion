from .tool import Tool


def wrap_for_fusion(tools: list[Tool]) -> str:
    """Adds header and footer to a sequence of tools"""

    tools_string = "".join([str(tool) for tool in tools])

    header = "{\n\tTools = ordered() {\n"
    footer = f'\t}},\n\tActiveTool = "{tools[-1].name}"\n}}'

    return header + tools_string + footer
