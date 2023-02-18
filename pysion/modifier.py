from .tool import Tool


class Modifier(Tool):
    def __init__(self, id: str, name: str) -> None:
        return super().__init__(id, name, position=None)
