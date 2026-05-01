from google.cloud import compute_v1
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gcp_vpcs() -> dict:
    """Lista todas as VPC Networks no GCP."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = compute_v1.NetworksClient()
        request = compute_v1.ListNetworksRequest(project=settings.gcp.project_id)
        response = client.list(request=request)

        networks = [{"name": net.name, "auto_create_subnetworks": net.auto_create_subnetworks} for net in response]
        
        BaseTool.log_call("list_gcp_vpcs", provider="gcp", count=len(networks))
        return {"networks": networks, "count": len(networks)}
    except Exception as e:
        BaseTool.log_error("list_gcp_vpcs", "gcp", e)
        raise CloudToolError(f"Erro ao listar VPCs GCP: {str(e)}", provider="gcp")