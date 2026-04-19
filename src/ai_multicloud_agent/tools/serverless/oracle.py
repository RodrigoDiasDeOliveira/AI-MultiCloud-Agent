# src/ai_multicloud_agent/tools/serverless/oracle.py

from fastmcp import tool
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oci_functions() -> dict:
    """Lista funções no Oracle Cloud Functions (OCI)."""
    # OCI Functions usa o mesmo client de applications
    BaseTool.log_call("list_oci_functions", provider="oracle")
    return {
        "message": "Oracle Cloud Functions será implementado em breve. Use o console OCI por enquanto.",
        "status": "placeholder"
    }