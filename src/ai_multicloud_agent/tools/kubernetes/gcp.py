# src/ai_multicloud_agent/tools/kubernetes/gcp.py

from google.cloud import container_v1
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gke_clusters(location: str = "-") -> dict:
    """Lista todos os clusters GKE no Google Cloud."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = container_v1.ClusterManagerClient()
        parent = f"projects/{settings.gcp.project_id}/locations/{location}"

        response = client.list_clusters(parent=parent)

        clusters = []
        for cluster in response.clusters:
            clusters.append({
                "name": cluster.name,
                "location": cluster.location,
                "version": cluster.current_master_version,
                "node_count": sum(pool.initial_node_count for pool in cluster.node_pools),
                "status": cluster.status.name
            })

        BaseTool.log_call("list_gke_clusters", provider="gcp", count=len(clusters))
        return {"gke_clusters": clusters, "count": len(clusters)}
    except Exception as e:
        BaseTool.log_error("list_gke_clusters", "gcp", e)
        raise CloudToolError(f"Erro ao listar clusters GKE: {str(e)}", provider="gcp")


@tool
def get_gke_kubeconfig(cluster_name: str, location: str = "us-central1") -> str:
    """Gera comando para obter kubeconfig de um cluster GKE."""
    BaseTool.log_call("get_gke_kubeconfig", provider="gcp", cluster=cluster_name)
    return (
        f"Comando para configurar kubeconfig do GKE:\n"
        f"gcloud container clusters get-credentials {cluster_name} "
        f"--location {location} --project {settings.gcp.project_id}"
    )