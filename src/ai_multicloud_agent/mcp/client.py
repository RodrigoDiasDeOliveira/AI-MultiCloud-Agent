# src/ai_multicloud_agent/mcp/client.py  (Versão Melhorada)

from mcp.client import ClientSession
from mcp.client.sse import sse_client
from langchain_core.tools import BaseTool
from pydantic import Field
from typing import List, Dict, Any
import structlog

logger = structlog.get_logger()

class MCPToolWrapper:
    """Wrapper avançado que conecta todas as tools do MCP ao LangGraph."""

    def __init__(self):
        self.session = None
        self._tools: List[BaseTool] = []

    async def connect(self):
        """Conecta ao MCP Server."""
        try:
            transport = await sse_client("http://localhost:8000")
            self.session = ClientSession(transport)
            await self.session.__aenter__()
            logger.info("mcp_client_connected")
            await self.load_tools()
            return True
        except Exception as e:
            logger.error("mcp_connection_failed", error=str(e))
            return False

    async def load_tools(self):
        """Carrega dinamicamente todas as tools do MCP."""
        if not self.session:
            await self.connect()

        tools_response = await self.session.list_tools()
        self._tools = []

        for tool in tools_response.tools:
            langchain_tool = self._create_dynamic_tool(tool)
            self._tools.append(langchain_tool)

        logger.info("tools_loaded", count=len(self._tools))

    def _create_dynamic_tool(self, mcp_tool):
        class DynamicTool(BaseTool):
            name: str = mcp_tool.name
            description: str = mcp_tool.description or f"Executa tool MCP: {mcp_tool.name}"
            args_schema: Any = mcp_tool.input_schema if hasattr(mcp_tool, 'input_schema') else None

            async def _arun(self, **kwargs):
                try:
                    result = await self.session.call_tool(mcp_tool.name, kwargs)
                    return result.content[0].text if result.content else "OK"
                except Exception as e:
                    logger.error("tool_execution_error", tool=mcp_tool.name, error=str(e))
                    return f"Erro ao executar {mcp_tool.name}: {str(e)}"

        return DynamicTool()

    def get_all_tools(self) -> List[BaseTool]:
        return self._tools