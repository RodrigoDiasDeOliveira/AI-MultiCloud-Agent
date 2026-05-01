"""Azure provider adapter for AI MultiCloud Agent."""

from ai_multicloud_agent.core.provider_base import BaseCloudProvider
from ai_multicloud_agent.config.settings import settings


class AzureProvider(BaseCloudProvider):
    name = "azure"

    def get_tools(self) -> list[str]:
        return [
            "azure_create_vm",
            "azure_list_vms",
        ]

    def health_check(self) -> dict[str, str]:
        status = (
            "ok"
            if settings.azure.subscription_id and settings.azure.client_id and settings.azure.tenant_id
            else "missing_credentials"
        )
        return {
            "provider": self.name,
            "status": status,
            "subscription_id": settings.azure.subscription_id or "not_configured",
        }
