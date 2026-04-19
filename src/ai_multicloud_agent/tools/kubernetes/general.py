from fastmcp import tool
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

# Ferramenta genérica que pode ser usada por qualquer provedor
@tool
def get_kubernetes_info(cluster_name: str, provider: str) -> dict:
    """Retorna informações básicas de um cluster Kubernetes (genérico)."""
    BaseTool.log_call("get_kubernetes_info", provider=provider, cluster=cluster_name)
    return {
        "cluster_name": cluster_name,
        "provider": provider,
        "status": "running",
        "message": f"Informações do cluster {cluster_name} no {provider} serão expandidas em breve."
    }