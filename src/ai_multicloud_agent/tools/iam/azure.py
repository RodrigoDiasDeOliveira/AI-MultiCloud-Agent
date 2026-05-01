from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_azure_role_assignments(resource_group: str = None) -> dict:
    """Lista atribuições de roles no Azure."""
    try:
        credential = DefaultAzureCredential()
        auth_client = AuthorizationManagementClient(credential, settings.azure.subscription_id)

        assignments = auth_client.role_assignments.list()
        roles = [{"principal": a.principal_id, "role": a.role_definition_id} for a in assignments]

        BaseTool.log_call("list_azure_role_assignments", provider="azure", count=len(roles))
        return {"role_assignments": roles, "count": len(roles)}
    except Exception as e:
        BaseTool.log_error("list_azure_role_assignments", "azure", e)
        raise CloudToolError(f"Erro ao listar role assignments: {str(e)}", provider="azure")
