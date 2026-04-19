# src/ai_multicloud_agent/tools/kubernetes/oracle.py

import oci
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oke_clusters() -> dict:
    """Lista todos os clusters Kubernetes (OKE) na Oracle Cloud."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        client = oci.container_engine.ContainerEngineClient(config)

        clusters = client.list_clusters(compartment_id=settings.oracle.compartment_id)
        
        cluster_list = []
        for cluster in clusters.data:
            cluster_list.append({
                "id": cluster.id,
                "name": cluster.name,
                "kubernetes_version": cluster.kubernetes_version,
                "lifecycle_state": cluster.lifecycle_state,
                "endpoint": cluster.endpoints.kubernetes
            })

        BaseTool.log_call("list_oke_clusters", provider="oracle", count=len(cluster_list))
        return {"oke_clusters": cluster_list, "count": len(cluster_list)}
    except Exception as e:
        BaseTool.log_error("list_oke_clusters", "oracle", e)
        raise CloudToolError(f"Erro ao listar clusters OKE: {str(e)}", provider="oracle")


@tool
def get_oke_kubeconfig(cluster_id: str) -> str:
    """Obtém informações para configurar kubeconfig de um cluster OKE."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        client = oci.container_engine.ContainerEngineClient(config)

        kubeconfig = client.create_kubeconfig(
            cluster_id=cluster_id,
            create_kubeconfig_details=oci.container_engine.models.CreateKubeconfigDetails(
                expiration=2592000,  # 30 dias
                token_version="2.0.0"
            )
        )

        BaseTool.log_call("get_oke_kubeconfig", provider="oracle", cluster_id=cluster_id)
        return f"Kubeconfig gerado para o cluster OKE {cluster_id}. Salve o conteúdo em ~/.kube/config"
    except Exception as e:
        BaseTool.log_error("get_oke_kubeconfig", "oracle", e)
        raise CloudToolError(f"Erro ao gerar kubeconfig OKE: {str(e)}", provider="oracle")