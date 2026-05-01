from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_azure_monitor_alerts(resource_group: str = None) -> dict:
    """Lista alertas do Azure Monitor."""
    try:
        credential = DefaultAzureCredential()
        monitor_client = MonitorManagementClient(credential, settings.azure.subscription_id)

        alerts = monitor_client.activity_log_alerts.list_by_subscription() if not resource_group else \
                 monitor_client.activity_log_alerts.list_by_resource_group(resource_group)

        alert_list = [alert.name for alert in alerts]
        BaseTool.log_call("list_azure_monitor_alerts", provider="azure", count=len(alert_list))
        return {"alerts": alert_list, "count": len(alert_list)}
    except Exception as e:
        BaseTool.log_error("list_azure_monitor_alerts", "azure", e)
        raise CloudToolError(f"Erro ao listar alertas Azure Monitor: {str(e)}", provider="azure")
