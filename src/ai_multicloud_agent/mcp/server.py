from fastapi import FastAPI

from ai_multicloud_agent.tools.registry import register_tools


def create_mcp_app() -> FastAPI:
    app = FastAPI(title="AI MultiCloud Agent MCP Server")
    register_tools(app)
    return app
