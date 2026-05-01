import boto3
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_eks_clusters(region: str = None) -> dict:
    """Lista clusters EKS na AWS."""
    try:
        client = boto3.client(
            'eks',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.list_clusters()
        BaseTool.log_call("list_eks_clusters", provider="aws", count=len(response['clusters']))
        return {"eks_clusters": response['clusters'], "count": len(response['clusters'])}
    except Exception as e:
        BaseTool.log_error("list_eks_clusters", "aws", e)
        raise CloudToolError(f"Erro ao listar clusters EKS: {str(e)}", provider="aws")