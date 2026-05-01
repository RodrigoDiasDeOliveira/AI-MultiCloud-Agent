from google.cloud import compute_v1
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gcp_instances(zone: str = "us-central1-a") -> dict:
    """Lista instâncias de Compute Engine no GCP."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path
        instance_client = compute_v1.InstancesClient()
        request = compute_v1.ListInstancesRequest(project=settings.gcp.project_id, zone=zone)
        response = instance_client.list(request=request)
        instances = [{"name": inst.name, "status": inst.status, "machine_type": inst.machine_type} for inst in response]
        BaseTool.log_call("list_gcp_instances", count=len(instances))
        return {"instances": instances, "count": len(instances)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar instâncias GCP: {str(e)}")