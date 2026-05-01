import boto3
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_s3_buckets(region: str = None) -> dict:
    """Lista todos os buckets S3 na conta AWS."""
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        BaseTool.log_call("list_s3_buckets", count=len(buckets))
        return {"buckets": buckets, "count": len(buckets)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar buckets S3: {str(e)}")

@tool
def create_s3_bucket(bucket_name: str, region: str = None) -> str:
    """Cria um novo bucket S3."""
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region or settings.aws.region}
        )
        BaseTool.log_call("create_s3_bucket", bucket=bucket_name)
        return f"Bucket {bucket_name} criado com sucesso na região {region or settings.aws.region}"
    except Exception as e:
        raise CloudToolError(f"Erro ao criar bucket S3: {str(e)}")

@tool
def upload_to_s3(bucket_name: str, key: str, content: str, region: str = None) -> str:
    """Faz upload de conteúdo (texto) para um bucket S3. Use base64 para arquivos binários."""
    try:
        client = boto3.client('s3', 
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        client.put_object(Bucket=bucket_name, Key=key, Body=content.encode())
        BaseTool.log_call("upload_to_s3", bucket=bucket_name, key=key)
        return f"Arquivo {key} enviado com sucesso para {bucket_name}"
    except Exception as e:
        raise CloudToolError(f"Erro no upload para S3: {str(e)}")