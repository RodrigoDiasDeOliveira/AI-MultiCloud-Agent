from pydantic import BaseSettings, Field, SecretStr


class CloudCredentials(BaseSettings):
    access_key_id: str | None = Field(None, env="AWS_ACCESS_KEY_ID")
    secret_access_key: SecretStr | None = Field(None, env="AWS_SECRET_ACCESS_KEY")
    region: str | None = Field(None, env="AWS_REGION")

    model_config = {
        "extra": "ignore",
    }


class Settings(BaseSettings):
    app_env: str = Field("development", env="APP_ENV")
    app_host: str = Field("0.0.0.0", env="APP_HOST")
    app_port: int = Field(8000, env="APP_PORT")

    aws: CloudCredentials = CloudCredentials()
    azure_tenant_id: str | None = Field(None, env="AZURE_TENANT_ID")
    azure_client_id: str | None = Field(None, env="AZURE_CLIENT_ID")
    azure_client_secret: SecretStr | None = Field(None, env="AZURE_CLIENT_SECRET")
    azure_subscription_id: str | None = Field(None, env="AZURE_SUBSCRIPTION_ID")
    gcp_project_id: str | None = Field(None, env="GCP_PROJECT_ID")
    oracle_tenancy: str | None = Field(None, env="ORACLE_CLOUD_TENANCY")
    oracle_user: str | None = Field(None, env="ORACLE_CLOUD_USER")
    oracle_fingerprint: str | None = Field(None, env="ORACLE_CLOUD_FINGERPRINT")
    oracle_private_key_file: str | None = Field(None, env="ORACLE_CLOUD_PRIVATE_KEY_FILE")

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
