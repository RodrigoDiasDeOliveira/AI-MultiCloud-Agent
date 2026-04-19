# src/ai_multicloud_agent/tools/monitoring/oracle.py

import oci
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oci_monitoring_alarms() -> dict:
    """Lista alarmes configurados no Oracle Monitoring."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        monitoring_client = oci.monitoring.MonitoringClient(config)

        alarms = monitoring_client.list_alarms(compartment_id=settings.oracle.compartment_id)
        alarm_list = [{"id": a.id, "display_name": a.display_name, "state": a.lifecycle_state} for a in alarms.data]

        BaseTool.log_call("list_oci_monitoring_alarms", provider="oracle", count=len(alarm_list))
        return {"alarms": alarm_list, "count": len(alarm_list)}
    except Exception as e:
        BaseTool.log_error("list_oci_monitoring_alarms", "oracle", e)
        raise CloudToolError(f"Erro ao listar alarmes OCI: {str(e)}", provider="oracle")