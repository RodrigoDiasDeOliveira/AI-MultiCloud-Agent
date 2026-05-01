from google.cloud import sql_v1
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError, ValidationError
import os

@tool
def create_gcp_postgresql_instance(
    instance_name: str,
    region: str = "us-central1",
    tier: str = "db-f1-micro",
    storage_gb: int = 10,
    password: str = None
) -> str:
    """Cria uma instância Cloud SQL com PostgreSQL no GCP."""
    if not password:
        raise ValidationError("password é obrigatório")

    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = sql_v1.SqlInstancesServiceClient()

        instance_body = {
            "name": instance_name,
            "region": region,
            "databaseVersion": "POSTGRES_16",
            "settings": {
                "tier": tier,
                "dataDiskSizeGb": storage_gb,
                "passwordValidationPolicy": {"minLength": 8}
            },
            "rootPassword": password
        }

        operation = client.insert(
            project=settings.gcp.project_id,
            body=instance_body
        )
        operation.result()  # Aguarda conclusão

        BaseTool.log_call("create_gcp_postgresql_instance", provider="gcp", instance_name=instance_name)
        return f"Instância Cloud SQL PostgreSQL '{instance_name}' criada com sucesso no GCP."
    except Exception as e:
        BaseTool.log_error("create_gcp_postgresql_instance", "gcp", e)
        raise CloudToolError(f"Erro ao criar Cloud SQL PostgreSQL: {str(e)}", provider="gcp")
