"""Oracle Cloud provider adapter for AI MultiCloud Agent."""

from ai_multicloud_agent.core.provider_base import BaseCloudProvider
from ai_multicloud_agent.config.settings import settings


class OracleProvider(BaseCloudProvider):
    name = "oracle"

    def get_tools(self) -> list[str]:
        return [
            "oci_create_instance",
        ]

    def health_check(self) -> dict[str, str]:
        status = (
            "ok"
            if settings.oracle.compartment_id and settings.oracle.namespace
            else "missing_credentials"
        )
        return {
            "provider": self.name,
            "status": status,
            "compartment_id": settings.oracle.compartment_id or "not_configured",
        }
