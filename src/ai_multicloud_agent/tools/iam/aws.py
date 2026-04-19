import boto3
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError, ValidationError

@tool
def list_iam_users() -> dict:
    """Lista todos os usuários IAM na conta AWS."""
    try:
        client = boto3.client(
            'iam',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key
        )
        response = client.list_users()
        users = [user['UserName'] for user in response['Users']]
        BaseTool.log_call("list_iam_users", provider="aws", count=len(users))
        return {"users": users, "count": len(users)}
    except Exception as e:
        BaseTool.log_error("list_iam_users", "aws", e)
        raise CloudToolError(f"Erro ao listar usuários IAM: {str(e)}", provider="aws")


@tool
def create_iam_user(username: str) -> str:
    """Cria um novo usuário IAM."""
    try:
        client = boto3.client(
            'iam',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key
        )
        client.create_user(UserName=username)
        BaseTool.log_call("create_iam_user", provider="aws", username=username)
        return f"Usuário IAM '{username}' criado com sucesso."
    except Exception as e:
        BaseTool.log_error("create_iam_user", "aws", e)
        raise CloudToolError(f"Erro ao criar usuário IAM: {str(e)}", provider="aws")


@tool
def create_iam_role(role_name: str, assume_role_policy: str = None) -> str:
    """Cria uma Role IAM (padrão para EC2 se não informado policy)."""
    if not assume_role_policy:
        assume_role_policy = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

    try:
        client = boto3.client('iam', 
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key
        )
        response = client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy
        )
        BaseTool.log_call("create_iam_role", provider="aws", role_name=role_name)
        return f"Role IAM '{role_name}' criada com sucesso."
    except Exception as e:
        BaseTool.log_error("create_iam_role", "aws", e)
        raise CloudToolError(f"Erro ao criar Role IAM: {str(e)}", provider="aws")