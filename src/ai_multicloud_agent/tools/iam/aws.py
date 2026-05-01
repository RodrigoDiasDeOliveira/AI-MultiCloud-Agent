import boto3
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError


def _iam_client():
    return boto3.client(
        "iam",
        aws_access_key_id=settings.aws.access_key_id_resolved,
        aws_secret_access_key=settings.aws.secret_access_key_resolved,
    )


@tool
def aws_list_roles() -> dict:
    """Lista Roles IAM na conta AWS."""
    try:
        client = _iam_client()
        response = client.list_roles()
        roles = [role["RoleName"] for role in response.get("Roles", [])]
        BaseTool.log_call("aws_list_roles", provider="aws", count=len(roles))
        return {"roles": roles, "count": len(roles)}
    except Exception as e:
        BaseTool.log_error("aws_list_roles", "aws", e)
        raise CloudToolError(f"Erro ao listar roles IAM: {str(e)}", provider="aws")


@tool
def aws_get_policy(policy_arn: str) -> dict:
    """Retorna os detalhes de uma política IAM pelo ARN."""
    try:
        client = _iam_client()
        response = client.get_policy(PolicyArn=policy_arn)
        policy = response.get("Policy", {})
        BaseTool.log_call("aws_get_policy", provider="aws", policy_arn=policy_arn)
        return {"policy": policy}
    except Exception as e:
        BaseTool.log_error("aws_get_policy", "aws", e)
        raise CloudToolError(f"Erro ao buscar policy IAM: {str(e)}", provider="aws")
