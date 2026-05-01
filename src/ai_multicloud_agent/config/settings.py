from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

from ai_multicloud_agent.utils.security import resolve_secret


class AWSSettings(BaseSettings):
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    region: str = "us-east-1"

    @property
    def access_key_id_resolved(self) -> Optional[str]:
        return self.access_key_id or resolve_secret("aws", "AWS_ACCESS_KEY_ID")

    @property
    def secret_access_key_resolved(self) -> Optional[str]:
        return self.secret_access_key or resolve_secret("aws", "AWS_SECRET_ACCESS_KEY")


class AzureSettings(BaseSettings):
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    subscription_id: Optional[str] = None
    # Para simplicidade inicial (Blob Storage). Em produção, use DefaultAzureCredential
    connection_string: Optional[str] = None


class GCPSettings(BaseSettings):
    project_id: Optional[str] = None
    # Caminho para o arquivo JSON de credenciais (recomendado)
    credentials_path: Optional[str] = None


class OracleSettings(BaseSettings):
    config_file: Optional[str] = "~/.oci/config"   # caminho padrão do OCI CLI
    profile: str = "DEFAULT"
    # Namespace é obrigatório no OCI Object Storage
    namespace: Optional[str] = None
    compartment_id: Optional[str] = None   # Necessário para muitas operações


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_nested_delimiter="__"   # permite AWS__REGION no .env
    )

    mcp_server_name: str = "AI-MultiCloud-Agent"
    log_level: str = "INFO"
    environment: str = "development"

    aws: AWSSettings = AWSSettings()
    azure: AzureSettings = AzureSettings()
    gcp: GCPSettings = GCPSettings()
    oracle: OracleSettings = OracleSettings()

    @property
    def aws_credentials(self) -> dict[str, str]:
        credentials: dict[str, str] = {}
        if self.aws.access_key_id_resolved:
            credentials["aws_access_key_id"] = self.aws.access_key_id_resolved
        if self.aws.secret_access_key_resolved:
            credentials["aws_secret_access_key"] = self.aws.secret_access_key_resolved
        return credentials


settings = Settings()
