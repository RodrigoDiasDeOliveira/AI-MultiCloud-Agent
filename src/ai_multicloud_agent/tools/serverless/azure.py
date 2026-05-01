# src/ai_multicloud_agent/tools/serverless/azure.py

from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_azure_function_apps(resource_group: str = None) -> dict:
    """Lista todas as Function Apps no Azure."""
    try:
        credential = DefaultAzureCredential()
        client = WebSiteManagementClient(credential, settings.azure.subscription_id)

        if resource_group:
            apps = client.web_apps.list_by_resource_group(resource_group)
        else:
            apps = client.web_apps.list()

        function_apps = [
            {"name": app.name, "location": app.location, "kind": app.kind}
            for app in apps if "function" in str(app.kind).lower()
        ]

        BaseTool.log_call("list_azure_function_apps", provider="azure", count=len(function_apps))
        return {"function_apps": function_apps, "count": len(function_apps)}
    except Exception as e:
        BaseTool.log_error("list_azure_function_apps", "azure", e)
        raise CloudToolError(f"Erro ao listar Function Apps: {str(e)}", provider="azure")