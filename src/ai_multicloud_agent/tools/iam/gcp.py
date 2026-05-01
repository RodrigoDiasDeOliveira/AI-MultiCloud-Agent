# src/ai_multicloud_agent/tools/iam/gcp.py

from google.cloud import iam_admin_v1
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gcp_service_accounts() -> dict:
    """Lista todas as Service Accounts no GCP."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = iam_admin_v1.IAMClient()
        request = iam_admin_v1.ListServiceAccountsRequest(
            name=f"projects/{settings.gcp.project_id}"
        )
        response = client.list_service_accounts(request=request)

        accounts = [{"email": sa.email, "name": sa.name} for sa in response]
        BaseTool.log_call("list_gcp_service_accounts", provider="gcp", count=len(accounts))
        return {"service_accounts": accounts, "count": len(accounts)}
    except Exception as e:
        BaseTool.log_error("list_gcp_service_accounts", "gcp", e)
        raise CloudToolError(f"Erro ao listar Service Accounts GCP: {str(e)}", provider="gcp")


@tool
def create_gcp_service_account(account_id: str, display_name: str = None) -> str:
    """Cria uma nova Service Account no GCP."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = iam_admin_v1.IAMClient()
        request = iam_admin_v1.CreateServiceAccountRequest(
            name=f"projects/{settings.gcp.project_id}",
            account_id=account_id,
            service_account={
                "display_name": display_name or account_id
            }
        )
        account = client.create_service_account(request=request)

        BaseTool.log_call("create_gcp_service_account", provider="gcp", account_id=account_id)
        return f"Service Account '{account.email}' criada com sucesso no GCP."
    except Exception as e:
        BaseTool.log_error("create_gcp_service_account", "gcp", e)
        raise CloudToolError(f"Erro ao criar Service Account GCP: {str(e)}", provider="gcp")