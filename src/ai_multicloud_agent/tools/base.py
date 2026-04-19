from fastapi import FastAPI


class BaseTool:
    def __init__(self, name: str) -> None:
        self.name = name

    def register(self, app: FastAPI) -> None:
        setattr(app.state, self.name, self)
