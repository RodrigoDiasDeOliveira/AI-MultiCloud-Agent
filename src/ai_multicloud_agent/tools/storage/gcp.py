from google.cloud import storage
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gcp_buckets() -> dict:
    """Lista todos os buckets no Google Cloud Storage."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path
        client = storage.Client(project=settings.gcp.project_id)
        buckets = [bucket.name for bucket in client.list_buckets()]
        BaseTool.log_call("list_gcp_buckets", count=len(buckets))
        return {"buckets": buckets, "count": len(buckets)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar buckets GCP: {str(e)}")

@tool
def create_gcp_bucket(bucket_name: str, location: str = "US") -> str:
    """Cria um novo bucket no Google Cloud Storage."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path
        client = storage.Client(project=settings.gcp.project_id)
        bucket = client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        new_bucket = client.create_bucket(bucket, location=location)
        BaseTool.log_call("create_gcp_bucket", bucket=bucket_name, location=location)
        return f"Bucket {new_bucket.name} criado com sucesso na localização {location}"
    except Exception as e:
        raise CloudToolError(f"Erro ao criar bucket GCP: {str(e)}")