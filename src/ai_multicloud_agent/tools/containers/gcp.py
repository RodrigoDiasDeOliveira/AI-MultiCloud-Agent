from google.cloud import container_v1
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gke_clusters() -> dict:
    """Lista clusters GKE no Google Cloud."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = container_v1.ClusterManagerClient()
        parent = f"projects/{settings.gcp.project_id}/locations/-"
        response = client.list_clusters(parent=parent)

        clusters = [{"name": c.name, "location": c.location, "version": c.current_master_version} for c in response.clusters]
        BaseTool.log_call("list_gke_clusters", provider="gcp", count=len(clusters))
        return {"gke_clusters": clusters, "count": len(clusters)}
    except Exception as e:
        BaseTool.log_error("list_gke_clusters", "gcp", e)
        raise CloudToolError(f"Erro ao listar clusters GKE: {str(e)}", provider="gcp")