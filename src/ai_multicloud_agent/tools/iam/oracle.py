# src/ai_multicloud_agent/tools/iam/oracle.py

import oci
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oci_users() -> dict:
    """Lista usuários IAM na Oracle OCI."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        identity_client = oci.identity.IdentityClient(config)

        users = identity_client.list_users(compartment_id=settings.oracle.compartment_id)
        user_list = [{"id": u.id, "name": u.name, "description": u.description} for u in users.data]

        BaseTool.log_call("list_oci_users", provider="oracle", count=len(user_list))
        return {"users": user_list, "count": len(user_list)}
    except Exception as e:
        BaseTool.log_error("list_oci_users", "oracle", e)
        raise CloudToolError(f"Erro ao listar usuários OCI: {str(e)}", provider="oracle")