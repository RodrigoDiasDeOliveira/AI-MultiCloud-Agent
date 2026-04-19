# src/ai_multicloud_agent/tools/containers/oracle.py

import oci
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oci_container_instances() -> dict:
    """Lista Container Instances no Oracle Cloud."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        client = oci.container_instances.ContainerInstancesClient(config)

        instances = client.list_container_instances(compartment_id=settings.oracle.compartment_id)
        inst_list = [{"id": i.id, "display_name": i.display_name, "state": i.lifecycle_state} for i in instances.data]

        BaseTool.log_call("list_oci_container_instances", provider="oracle", count=len(inst_list))
        return {"container_instances": inst_list, "count": len(inst_list)}
    except Exception as e:
        BaseTool.log_error("list_oci_container_instances", "oracle", e)
        raise CloudToolError(f"Erro ao listar Container Instances OCI: {str(e)}", provider="oracle")