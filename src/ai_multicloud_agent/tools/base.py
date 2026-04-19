# src/ai_multicloud_agent/tools/base.py

import structlog
from typing import Any, Dict

logger = structlog.get_logger()

class BaseTool:
    """Classe base para todas as tools com logging padronizado e seguro."""

    @staticmethod
    def log_call(tool_name: str, provider: str = None, **kwargs):
        """Registra a chamada da tool de forma estruturada."""
        log_data: Dict[str, Any] = {
            "tool": tool_name,
            "provider": provider,
            **kwargs
        }
        logger.info("tool_called", **log_data)

    @staticmethod
    def log_error(tool_name: str, provider: str, error: Exception):
        """Registra erros de forma estruturada."""
        logger.error(
            "tool_error",
            tool=tool_name,
            provider=provider,
            error_type=type(error).__name__,
            error_message=str(error)
        )