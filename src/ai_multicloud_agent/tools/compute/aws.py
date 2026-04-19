import boto3
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_ec2_instances(region: str = None) -> dict:
    """Lista todas as instâncias EC2 em execução."""
    try:
        client = boto3.client(
            'ec2',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    "instance_id": instance['InstanceId'],
                    "state": instance['State']['Name'],
                    "type": instance['InstanceType'],
                    "region": region or settings.aws.region
                })
        BaseTool.log_call("list_ec2_instances", count=len(instances))
        return {"instances": instances, "count": len(instances)}
    except Exception as e:
        raise CloudToolError(f"Erro ao listar instâncias EC2: {str(e)}")

@tool
def create_ec2_instance(instance_type: str = "t3.micro", 
                       image_id: str = "ami-0c55b159cbfafe1f0",  # Amazon Linux 2 exemplo
                       region: str = None) -> str:
    """Cria uma instância EC2 básica."""
    try:
        client = boto3.client('ec2', 
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        BaseTool.log_call("create_ec2_instance", instance_id=instance_id, type=instance_type)
        return f"Instância EC2 {instance_id} criada com sucesso (tipo {instance_type})"
    except Exception as e:
        raise CloudToolError(f"Erro ao criar instância EC2: {str(e)}")