from ai_multicloud_agent.core.registry import ToolRegistry


def register_all_tools(mcp):
    """Registra todas as tools do AI-MultiCloud-Agent usando a camada core."""
    ToolRegistry().register_all_tools(mcp)
