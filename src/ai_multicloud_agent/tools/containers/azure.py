from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_aks_clusters(resource_group: str = None) -> dict:
    """Lista clusters Kubernetes (AKS) no Azure."""
    try:
        credential = DefaultAzureCredential()
        client = ContainerServiceClient(credential, settings.azure.subscription_id)

        if resource_group:
            clusters = client.managed_clusters.list_by_resource_group(resource_group)
        else:
            clusters = client.managed_clusters.list()

        aks_list = [{"name": c.name, "location": c.location, "kubernetes_version": c.kubernetes_version} for c in clusters]
        BaseTool.log_call("list_aks_clusters", provider="azure", count=len(aks_list))
        return {"aks_clusters": aks_list, "count": len(aks_list)}
    except Exception as e:
        BaseTool.log_error("list_aks_clusters", "azure", e)
        raise CloudToolError(f"Erro ao listar clusters AKS: {str(e)}", provider="azure")
