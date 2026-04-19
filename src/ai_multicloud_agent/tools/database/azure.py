from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.identity import DefaultAzureCredential
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError, ValidationError

@tool
def create_azure_postgresql_flexible(
    server_name: str,
    resource_group: str,
    location: str = "eastus",
    sku: str = "Standard_B1ms",
    storage_gb: int = 32,
    admin_login: str = "postgres",
    admin_password: str = None
) -> str:
    """Cria um servidor Azure Database for PostgreSQL Flexible Server."""
    if not admin_password:
        raise ValidationError("admin_password é obrigatório")

    try:
        credential = DefaultAzureCredential()
        client = PostgreSQLManagementClient(credential, settings.azure.subscription_id)

        poller = client.servers.begin_create(
            resource_group_name=resource_group,
            server_name=server_name,
            parameters={
                "location": location,
                "sku": {"name": sku},
                "properties": {
                    "administratorLogin": admin_login,
                    "administratorLoginPassword": admin_password,
                    "version": "16",
                    "storage": {"storageSizeGB": storage_gb},
                    "backup": {"retentionDays": 7}
                }
            }
        )
        result = poller.result()

        BaseTool.log_call("create_azure_postgresql_flexible", provider="azure", server_name=server_name)
        return f"Servidor PostgreSQL Flexible '{server_name}' criado com sucesso no Azure."
    except Exception as e:
        BaseTool.log_error("create_azure_postgresql_flexible", "azure", e)
        raise CloudToolError(f"Erro ao criar PostgreSQL no Azure: {str(e)}", provider="azure")