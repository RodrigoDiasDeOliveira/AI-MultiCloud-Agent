import oci
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oci_vcns() -> dict:
    """Lista todas as Virtual Cloud Networks (VCN) na Oracle OCI."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        client = oci.core.VirtualNetworkClient(config)

        vcns = client.list_vcns(compartment_id=settings.oracle.compartment_id)
        vcn_list = [{"id": vcn.id, "display_name": vcn.display_name, "cidr_block": vcn.cidr_block} for vcn in vcns.data]

        BaseTool.log_call("list_oci_vcns", provider="oracle", count=len(vcn_list))
        return {"vcns": vcn_list, "count": len(vcn_list)}
    except Exception as e:
        BaseTool.log_error("list_oci_vcns", "oracle", e)
        raise CloudToolError(f"Erro ao listar VCNs OCI: {str(e)}", provider="oracle")