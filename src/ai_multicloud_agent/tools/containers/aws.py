import boto3
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_ecs_clusters(region: str = None) -> dict:
    """Lista todos os clusters ECS na AWS."""
    try:
        client = boto3.client(
            'ecs',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.list_clusters()
        clusters = [arn.split('/')[-1] for arn in response['clusterArns']]
        BaseTool.log_call("list_ecs_clusters", provider="aws", count=len(clusters))
        return {"clusters": clusters, "count": len(clusters)}
    except Exception as e:
        BaseTool.log_error("list_ecs_clusters", "aws", e)
        raise CloudToolError(f"Erro ao listar clusters ECS: {str(e)}", provider="aws")


@tool
def list_ecr_repositories(region: str = None) -> dict:
    """Lista repositórios ECR (Container Registry)."""
    try:
        client = boto3.client(
            'ecr',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.describe_repositories()
        repos = [repo['repositoryName'] for repo in response['repositories']]
        BaseTool.log_call("list_ecr_repositories", provider="aws", count=len(repos))
        return {"repositories": repos, "count": len(repos)}
    except Exception as e:
        BaseTool.log_error("list_ecr_repositories", "aws", e)
        raise CloudToolError(f"Erro ao listar repositórios ECR: {str(e)}", provider="aws")