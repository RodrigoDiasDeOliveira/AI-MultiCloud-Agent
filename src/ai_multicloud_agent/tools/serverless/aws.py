import boto3
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError, ValidationError

@tool
def list_lambda_functions(region: str = None) -> dict:
    """Lista todas as funções Lambda."""
    try:
        client = boto3.client(
            'lambda',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.list_functions()
        functions = [f['FunctionName'] for f in response['Functions']]
        BaseTool.log_call("list_lambda_functions", provider="aws", count=len(functions))
        return {"functions": functions, "count": len(functions)}
    except Exception as e:
        BaseTool.log_error("list_lambda_functions", "aws", e)
        raise CloudToolError(f"Erro ao listar funções Lambda: {str(e)}", provider="aws")


@tool
def create_lambda_function(
    function_name: str,
    runtime: str = "python3.12",
    role_arn: str = None,
    handler: str = "lambda_function.lambda_handler",
    zip_file_content: str = None   # base64 ou usar S3 em produção
) -> str:
    """Cria uma função Lambda básica (exemplo simplificado)."""
    if not role_arn:
        raise ValidationError("role_arn é obrigatório para criar Lambda")

    try:
        client = boto3.client('lambda', 
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=settings.aws.region
        )

        # Versão simplificada - em produção use upload via S3
        response = client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler,
            Code={"ZipFile": b"def lambda_handler(event, context):\n    return {'statusCode': 200}"},  # exemplo mínimo
            Description="Função criada pelo AI-MultiCloud-Agent"
        )

        BaseTool.log_call("create_lambda_function", provider="aws", function_name=function_name)
        return f"Função Lambda '{function_name}' criada com sucesso (Runtime: {runtime})"
    except Exception as e:
        BaseTool.log_error("create_lambda_function", "aws", e)
        raise CloudToolError(f"Erro ao criar função Lambda: {str(e)}", provider="aws")