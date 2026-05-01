"""GCP provider adapter for AI MultiCloud Agent."""

from ai_multicloud_agent.core.provider_base import BaseCloudProvider
from ai_multicloud_agent.config.settings import settings


class GCPProvider(BaseCloudProvider):
    name = "gcp"

    def get_tools(self) -> list[str]:
        return [
            "gcp_create_instance",
            "gcp_list_instances",
        ]

    def health_check(self) -> dict[str, str]:
        status = "ok" if settings.gcp.project_id else "missing_credentials"
        return {
            "provider": self.name,
            "status": status,
            "project_id": settings.gcp.project_id or "not_configured",
        }
