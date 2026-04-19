from azure.storage.blob import BlobServiceClient
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_azure_storage_accounts() -> dict:
    """Lista as storage accounts no Azure."""
    try:
        # Para simplicidade inicial, usa BlobServiceClient com connection string (melhorar depois com azure-identity)
        # Recomendado: usar DefaultAzureCredential em produção
        client = BlobServiceClient.from_connection_string(settings.azure.connection_string)  # adicione no settings depois
        containers = client.list_containers()
        container_list = [c.name for c in containers]
        BaseTool.log_call("list_azure_storage_accounts", count=len(container_list))
        return {"containers": container_list, "count": len(container_list)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar containers Azure: {str(e)}")

@tool
def create_azure_container(container_name: str) -> str:
    """Cria um container de blob no Azure."""
    try:
        client = BlobServiceClient.from_connection_string(settings.azure.connection_string)
        container_client = client.get_container_client(container_name)
        container_client.create_container()
        BaseTool.log_call("create_azure_container", container=container_name)
        return f"Container {container_name} criado com sucesso no Azure Blob Storage"
    except Exception as e:
        raise CloudToolError(f"Erro ao criar container Azure: {str(e)}")
