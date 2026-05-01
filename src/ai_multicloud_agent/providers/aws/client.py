from typing import Any
from ai_multicloud_agent.config.settings import AWSSettings
from ai_multicloud_agent.utils.security import resolve_secret


class AWSClient:
    def __init__(self, settings: AWSSettings) -> None:
        self.settings = settings

    def _import_boto3(self) -> Any:
        try:
            import boto3
        except ImportError as error:
            raise ImportError(
                "boto3 is required for AWS operations. Install it with `pip install .[aws]` or add boto3 to your environment."
            ) from error
        return boto3

    def _credentials(self) -> dict:
        return {
            "aws_access_key_id": self.settings.access_key_id or resolve_secret("aws", "AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": self.settings.secret_access_key or resolve_secret("aws", "AWS_SECRET_ACCESS_KEY"),
        }

    def ec2_client(self, region: str | None = None):
        boto3 = self._import_boto3()
        return boto3.client(
            "ec2",
            region_name=region or self.settings.region,
            **{k: v for k, v in self._credentials().items() if v is not None},
        )

    def iam_client(self):
        boto3 = self._import_boto3()
        return boto3.client(
            "iam",
            **{k: v for k, v in self._credentials().items() if v is not None},
        )

    def handle_error(self, error: Exception) -> str:
        try:
            from botocore.exceptions import ClientError
        except ImportError:
            return str(error)

        if isinstance(error, ClientError):
            return error.response.get("Error", {}).get("Message", str(error))
        return str(error)
