"""AWS provider adapter for AI MultiCloud Agent."""

from ai_multicloud_agent.core.provider_base import BaseCloudProvider
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.providers.aws.client import AWSClient


class AWSProvider(BaseCloudProvider):
    name = "aws"

    def __init__(self) -> None:
        self.client = AWSClient(settings.aws)

    def get_tools(self) -> list[str]:
        return [
            "aws_list_instances",
            "aws_create_ec2",
            "aws_stop_instance",
            "aws_list_roles",
            "aws_get_policy",
        ]

    def health_check(self) -> dict[str, str]:
        status = (
            "ok"
            if settings.aws.access_key_id_resolved and settings.aws.secret_access_key_resolved
            else "missing_credentials"
        )
        return {
            "provider": self.name,
            "region": settings.aws.region,
            "status": status,
        }
