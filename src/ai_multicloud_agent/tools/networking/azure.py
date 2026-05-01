from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_virtual_networks(resource_group: str = None) -> dict:
    """Lista Virtual Networks (VNet) no Azure."""
    try:
        credential = DefaultAzureCredential()
        network_client = NetworkManagementClient(credential, settings.azure.subscription_id)

        if resource_group:
            vn_list = network_client.virtual_networks.list(resource_group)
        else:
            vn_list = network_client.virtual_networks.list_all()

        vnets = [{"name": vnet.name, "location": vnet.location, "address_space": vnet.address_space.address_prefixes} 
                 for vnet in vn_list]
        
        BaseTool.log_call("list_virtual_networks", provider="azure", count=len(vnets))
        return {"vnets": vnets, "count": len(vnets)}
    except Exception as e:
        BaseTool.log_error("list_virtual_networks", "azure", e)
        raise CloudToolError(f"Erro ao listar Virtual Networks: {str(e)}", provider="azure")


@tool
def create_virtual_network(
    vnet_name: str,
    resource_group: str,
    location: str = "eastus",
    address_prefix: str = "10.0.0.0/16"
) -> str:
    """Cria uma Virtual Network no Azure."""
    try:
        credential = DefaultAzureCredential()
        network_client = NetworkManagementClient(credential, settings.azure.subscription_id)

        poller = network_client.virtual_networks.begin_create_or_update(
            resource_group_name=resource_group,
            virtual_network_name=vnet_name,
            parameters={
                "location": location,
                "address_space": {"address_prefixes": [address_prefix]}
            }
        )
        result = poller.result()

        BaseTool.log_call("create_virtual_network", provider="azure", vnet_name=vnet_name)
        return f"Virtual Network '{vnet_name}' criada com sucesso no Azure."
    except Exception as e:
        BaseTool.log_error("create_virtual_network", "azure", e)
        raise CloudToolError(f"Erro ao criar Virtual Network: {str(e)}", provider="azure")
