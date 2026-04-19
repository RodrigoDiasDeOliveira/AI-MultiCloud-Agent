import boto3
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError

@tool
def list_rds_instances(region: str = None) -> dict:
    """Lista todas as instâncias RDS (inclui PostgreSQL, MySQL, etc.)."""
    try:
        client = boto3.client(
            'rds',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )
        response = client.describe_db_instances()
        instances = []
        for db in response['DBInstances']:
            instances.append({
                "db_identifier": db['DBInstanceIdentifier'],
                "engine": db['Engine'],
                "status": db['DBInstanceStatus'],
                "class": db['DBInstanceClass'],
                "engine_version": db.get('EngineVersion')
            })
        BaseTool.log_call("list_rds_instances", provider="aws", count=len(instances))
        return {"instances": instances, "count": len(instances)}
    except Exception as e:
        BaseTool.log_error("list_rds_instances", "aws", e)
        raise CloudToolError(f"Erro ao listar instâncias RDS: {str(e)}", provider="aws")


@tool
def create_postgresql_rds(
    db_identifier: str,
    db_class: str = "db.t3.micro",
    storage: int = 20,
    username: str = "postgres",
    password: str = None,
    region: str = None
) -> str:
    """Cria uma instância RDS PostgreSQL."""
    if not password:
        raise ValidationError("Password é obrigatório para criar RDS PostgreSQL")

    try:
        client = boto3.client(
            'rds',
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=region or settings.aws.region
        )

        response = client.create_db_instance(
            DBInstanceIdentifier=db_identifier,
            DBInstanceClass=db_class,
            Engine='postgres',
            AllocatedStorage=storage,
            MasterUsername=username,
            MasterUserPassword=password,
            EngineVersion='16.3',          # Versão atual estável em 2026
            BackupRetentionPeriod=7,
            MultiAZ=False,
            PubliclyAccessible=True,
            Tags=[{'Key': 'ManagedBy', 'Value': 'AI-MultiCloud-Agent'}]
        )

        BaseTool.log_call("create_postgresql_rds", provider="aws", db_identifier=db_identifier)
        return f"Instância RDS PostgreSQL '{db_identifier}' criada com sucesso. Status: {response['DBInstance']['DBInstanceStatus']}"
    except Exception as e:
        BaseTool.log_error("create_postgresql_rds", "aws", e)
        raise CloudToolError(f"Erro ao criar RDS PostgreSQL: {str(e)}", provider="aws")