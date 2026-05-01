import boto3
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_cloudwatch_alarms(region: str = None) -> dict:
    """Lista alarmes configurados no CloudWatch."""
    try:
        client = boto3.client(
            'cloudwatch',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.describe_alarms()
        alarms = [alarm['AlarmName'] for alarm in response['MetricAlarms']]
        BaseTool.log_call("list_cloudwatch_alarms", provider="aws", count=len(alarms))
        return {"alarms": alarms, "count": len(alarms)}
    except Exception as e:
        BaseTool.log_error("list_cloudwatch_alarms", "aws", e)
        raise CloudToolError(f"Erro ao listar alarmes CloudWatch: {str(e)}", provider="aws")