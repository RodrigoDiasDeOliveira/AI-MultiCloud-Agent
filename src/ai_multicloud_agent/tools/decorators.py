from fastmcp.tools import tool
from functools import wraps
from typing import Callable


def mcp_tool(name: str, description: str, category: str, provider: str):
    """Decorator helper to create MCP tools with consistent metadata."""

    def decorator(func: Callable):
        wrapped = tool(func)
        wrapped.__name__ = name
        wrapped.__doc__ = description
        setattr(wrapped, "tool_category", category)
        setattr(wrapped, "tool_provider", provider)
        return wrapped

    return decorator
