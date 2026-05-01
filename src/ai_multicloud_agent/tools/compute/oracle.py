import oci
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oci_instances(compartment_id: str = None) -> dict:
    """Lista instâncias de Compute na Oracle OCI."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        compute_client = oci.core.ComputeClient(config)
        compartment = compartment_id or settings.oracle.compartment_id
        instances = compute_client.list_instances(compartment_id=compartment)
        inst_list = [{"id": i.id, "display_name": i.display_name, "shape": i.shape, "state": i.lifecycle_state} for i in instances.data]
        BaseTool.log_call("list_oci_instances", count=len(inst_list))
        return {"instances": inst_list, "count": len(inst_list)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar instâncias OCI: {str(e)}")
