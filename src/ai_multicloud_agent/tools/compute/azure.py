from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_azure_vms(resource_group: str = None) -> dict:
    """Lista máquinas virtuais no Azure (todas ou por resource group)."""
    try:
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, settings.azure.subscription_id)
        vms = []
        if resource_group:
            vm_list = compute_client.virtual_machines.list(resource_group)
        else:
            vm_list = compute_client.virtual_machines.list_all()
        for vm in vm_list:
            vms.append({"name": vm.name, "location": vm.location, "state": vm.power_state})
        BaseTool.log_call("list_azure_vms", count=len(vms))
        return {"vms": vms, "count": len(vms)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar VMs Azure: {str(e)}")

@tool
def create_azure_resource_group(resource_group_name: str, location: str = "eastus") -> str:
    """Cria um Resource Group no Azure (necessário antes de criar VMs)."""
    try:
        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, settings.azure.subscription_id)
        rg_result = resource_client.resource_groups.create_or_update(
            resource_group_name, {"location": location}
        )
        BaseTool.log_call("create_azure_resource_group", name=resource_group_name)
        return f"Resource Group {rg_result.name} criado em {location}"
    except Exception as e:
        raise CloudToolError(f"Erro ao criar Resource Group Azure: {str(e)}")
