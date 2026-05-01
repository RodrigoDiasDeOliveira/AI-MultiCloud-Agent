import boto3
from fastmcp.tools import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError


def _ec2_client(region: str | None = None):
    return boto3.client(
        "ec2",
        aws_access_key_id=settings.aws.access_key_id_resolved,
        aws_secret_access_key=settings.aws.secret_access_key_resolved,
        region_name=region or settings.aws.region,
    )


@tool
def aws_list_instances(region: str | None = None) -> dict:
    """Lista todas as instâncias EC2 em execução."""
    try:
        client = _ec2_client(region)
        response = client.describe_instances()
        instances = []
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances.append({
                    "instance_id": instance["InstanceId"],
                    "state": instance["State"]["Name"],
                    "type": instance["InstanceType"],
                    "region": region or settings.aws.region,
                })
        BaseTool.log_call("aws_list_instances", provider="aws", count=len(instances))
        return {"instances": instances, "count": len(instances)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar instâncias EC2: {str(e)}", provider="aws")


@tool
def aws_create_ec2(instance_type: str = "t3.micro", image_id: str = "ami-0c55b159cbfafe1f0", region: str | None = None) -> str:
    """Cria uma instância EC2 básica."""
    try:
        client = _ec2_client(region)
        response = client.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
        )
        instance_id = response["Instances"][0]["InstanceId"]
        BaseTool.log_call("aws_create_ec2", provider="aws", instance_id=instance_id, instance_type=instance_type)
        return f"Instância EC2 {instance_id} criada com sucesso (tipo {instance_type})"
    except Exception as e:
        raise CloudToolError(f"Erro ao criar instância EC2: {str(e)}", provider="aws")


@tool
def aws_stop_instance(instance_id: str, region: str | None = None) -> str:
    """Para uma instância EC2 especificada."""
    try:
        client = _ec2_client(region)
        client.stop_instances(InstanceIds=[instance_id])
        BaseTool.log_call("aws_stop_instance", provider="aws", instance_id=instance_id)
        return f"Instância EC2 {instance_id} solicitada para parada."
    except Exception as e:
        raise CloudToolError(f"Erro ao parar instância EC2: {str(e)}", provider="aws")
