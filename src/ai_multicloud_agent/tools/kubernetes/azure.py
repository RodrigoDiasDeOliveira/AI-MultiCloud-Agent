# src/ai_multicloud_agent/tools/kubernetes/azure.py

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_aks_clusters(resource_group: str = None) -> dict:
    """Lista todos os clusters Kubernetes (AKS) no Azure."""
    try:
        credential = DefaultAzureCredential()
        client = ContainerServiceClient(credential, settings.azure.subscription_id)

        if resource_group:
            clusters = client.managed_clusters.list_by_resource_group(resource_group)
        else:
            clusters = client.managed_clusters.list()

        aks_list = []
        for cluster in clusters:
            aks_list.append({
                "name": cluster.name,
                "location": cluster.location,
                "kubernetes_version": cluster.kubernetes_version,
                "provisioning_state": cluster.provisioning_state,
                "node_count": cluster.agent_pool_profiles[0].count if cluster.agent_pool_profiles else 0
            })

        BaseTool.log_call("list_aks_clusters", provider="azure", count=len(aks_list))
        return {"aks_clusters": aks_list, "count": len(aks_list)}
    except Exception as e:
        BaseTool.log_error("list_aks_clusters", "azure", e)
        raise CloudToolError(f"Erro ao listar clusters AKS: {str(e)}", provider="azure")


@tool
def get_aks_credentials(cluster_name: str, resource_group: str) -> str:
    """Obtém credenciais kubeconfig para um cluster AKS."""
    try:
        credential = DefaultAzureCredential()
        client = ContainerServiceClient(credential, settings.azure.subscription_id)

        creds = client.managed_clusters.list_cluster_admin_credentials(
            resource_group_name=resource_group,
            resource_name=cluster_name
        )

        BaseTool.log_call("get_aks_credentials", provider="azure", cluster=cluster_name)
        return f"Credenciais do cluster AKS '{cluster_name}' obtidas com sucesso. (Use 'az aks get-credentials' para configurar localmente)"
    except Exception as e:
        BaseTool.log_error("get_aks_credentials", "azure", e)
        raise CloudToolError(f"Erro ao obter credenciais AKS: {str(e)}", provider="azure")