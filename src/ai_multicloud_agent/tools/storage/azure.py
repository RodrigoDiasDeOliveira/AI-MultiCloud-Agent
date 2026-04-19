from ai_multicloud_agent.tools.base import BaseTool


class ${provider.capitalize()}${category.capitalize()}Tool(BaseTool):
    def __init__(self) -> None:
        super().__init__("${provider}_${category}")


def register(app):
    tool = ${provider.capitalize()}${category.capitalize()}Tool()
    tool.register(app)
