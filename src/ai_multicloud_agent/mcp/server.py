from fastmcp import FastMCP
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.utils.logging import setup_logging
from ai_multicloud_agent.tools.registry import register_all_tools

setup_logging(settings.log_level)

mcp = FastMCP(
    name=settings.mcp_server_name,
    version="0.1.0",
)

# Registra automaticamente todas as tools das categorias
register_all_tools(mcp)

if __name__ == "__main__":
    mcp.run()
