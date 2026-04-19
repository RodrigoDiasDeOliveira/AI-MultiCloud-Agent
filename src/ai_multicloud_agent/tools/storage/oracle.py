import oci
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_oci_buckets() -> dict:
    """Lista todos os buckets no Object Storage da Oracle OCI."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        client = oci.object_storage.ObjectStorageClient(config)
        namespace = settings.oracle.namespace or client.get_namespace().data
        buckets = client.list_buckets(namespace, settings.oracle.compartment_id)
        bucket_names = [b.name for b in buckets.data]
        BaseTool.log_call("list_oci_buckets", count=len(bucket_names))
        return {"buckets": bucket_names, "count": len(bucket_names), "namespace": namespace}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar buckets OCI: {str(e)}")

@tool
def create_oci_bucket(bucket_name: str) -> str:
    """Cria um novo bucket no Object Storage da Oracle OCI."""
    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        client = oci.object_storage.ObjectStorageClient(config)
        namespace = settings.oracle.namespace or client.get_namespace().data

        create_bucket_details = oci.object_storage.models.CreateBucketDetails(
            name=bucket_name,
            compartment_id=settings.oracle.compartment_id
        )
        client.create_bucket(namespace, create_bucket_details)
        BaseTool.log_call("create_oci_bucket", bucket=bucket_name)
        return f"Bucket {bucket_name} criado com sucesso no namespace {namespace}"
    except Exception as e:
        raise CloudToolError(f"Erro ao criar bucket OCI: {str(e)}")