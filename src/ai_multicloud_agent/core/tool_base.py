from pydantic import BaseModel
from typing import Optional


class ToolInput(BaseModel):
    """Base model for tool input validation."""


class BaseTool:
    """Base tool metadata and helpers."""

    name: str
    description: str
    category: str
    provider: str

    @classmethod
    def meta(cls) -> dict[str, str]:
        return {
            "name": getattr(cls, "name", "unknown"),
            "description": getattr(cls, "description", ""),
            "category": getattr(cls, "category", ""),
            "provider": getattr(cls, "provider", ""),
        }
