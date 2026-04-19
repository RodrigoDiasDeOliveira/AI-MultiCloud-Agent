from fastapi import FastAPI

from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.mcp.server import create_mcp_app

app: FastAPI = create_mcp_app()

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}
