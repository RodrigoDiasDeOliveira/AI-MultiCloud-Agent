from google.cloud import monitoring_v3
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gcp_alert_policies() -> dict:
    """Lista políticas de alertas no Google Cloud Monitoring."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = monitoring_v3.AlertPolicyServiceClient()
        parent = f"projects/{settings.gcp.project_id}"
        policies = client.list_alert_policies(name=parent)

        policy_names = [p.display_name for p in policies]
        BaseTool.log_call("list_gcp_alert_policies", provider="gcp", count=len(policy_names))
        return {"alert_policies": policy_names, "count": len(policy_names)}
    except Exception as e:
        BaseTool.log_error("list_gcp_alert_policies", "gcp", e)
        raise CloudToolError(f"Erro ao listar alert policies GCP: {str(e)}", provider="gcp")