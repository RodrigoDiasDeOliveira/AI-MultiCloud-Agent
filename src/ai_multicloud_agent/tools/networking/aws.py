import boto3
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError, ValidationError

@tool
def list_vpcs(region: str = None) -> dict:
    """Lista todas as VPCs na conta AWS."""
    try:
        client = boto3.client(
            'ec2',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.describe_vpcs()
        vpcs = [
            {
                "vpc_id": vpc['VpcId'],
                "cidr_block": vpc['CidrBlock'],
                "state": vpc['State'],
                "is_default": vpc.get('IsDefault', False)
            }
            for vpc in response['Vpcs']
        ]
        BaseTool.log_call("list_vpcs", provider="aws", count=len(vpcs))
        return {"vpcs": vpcs, "count": len(vpcs)}
    except Exception as e:
        BaseTool.log_error("list_vpcs", "aws", e)
        raise CloudToolError(f"Erro ao listar VPCs: {str(e)}", provider="aws")


@tool
def create_vpc(cidr_block: str = "10.0.0.0/16", region: str = None, name: str = None) -> str:
    """Cria uma nova VPC na AWS."""
    try:
        client = boto3.client(
            'ec2',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )

        response = client.create_vpc(CidrBlock=cidr_block)
        vpc_id = response['Vpc']['VpcId']

        # Adiciona tag Name se fornecido
        if name:
            client.create_tags(
                Resources=[vpc_id],
                Tags=[{'Key': 'Name', 'Value': name}]
            )

        BaseTool.log_call("create_vpc", provider="aws", vpc_id=vpc_id, cidr=cidr_block)
        return f"VPC {vpc_id} criada com sucesso com CIDR {cidr_block}"
    except Exception as e:
        BaseTool.log_error("create_vpc", "aws", e)
        raise CloudToolError(f"Erro ao criar VPC: {str(e)}", provider="aws")


@tool
def create_security_group(group_name: str, description: str, vpc_id: str, region: str = None) -> str:
    """Cria um Security Group na AWS."""
    try:
        client = boto3.client(
            'ec2',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )

        response = client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )
        sg_id = response['GroupId']

        BaseTool.log_call("create_security_group", provider="aws", sg_id=sg_id)
        return f"Security Group '{group_name}' ({sg_id}) criado com sucesso na VPC {vpc_id}"
    except Exception as e:
        BaseTool.log_error("create_security_group", "aws", e)
        raise CloudToolError(f"Erro ao criar Security Group: {str(e)}", provider="aws")