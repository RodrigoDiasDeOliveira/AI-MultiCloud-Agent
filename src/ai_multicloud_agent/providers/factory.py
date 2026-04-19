from typing import Any

from ai_multicloud_agent.providers.aws import AWSProvider
from ai_multicloud_agent.providers.azure import AzureProvider
from ai_multicloud_agent.providers.gcp import GCPProvider
from ai_multicloud_agent.providers.oracle import OracleProvider


class ProviderFactory:
    @staticmethod
    def create_provider(cloud: str) -> Any:
        providers = {
            "aws": AWSProvider,
            "azure": AzureProvider,
            "gcp": GCPProvider,
            "oracle": OracleProvider,
        }
        provider_cls = providers.get(cloud.lower())
        if provider_cls is None:
            raise ValueError(f"Unknown cloud provider: {cloud}")
        return provider_cls()
