import oci
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError, ValidationError

@tool
def create_oci_autonomous_database(
    db_name: str,
    admin_password: str = None,
    compute_count: float = 1,
    storage_tb: int = 1,
    db_version: str = "19c"
) -> str:
    """Cria um Autonomous Database (PostgreSQL ou Oracle) na OCI."""
    if not admin_password:
        raise ValidationError("admin_password é obrigatório")

    try:
        config = oci.config.from_file(settings.oracle.config_file, settings.oracle.profile)
        db_client = oci.database.DatabaseClient(config)

        create_details = oci.database.models.CreateAutonomousDatabaseDetails(
            compartment_id=settings.oracle.compartment_id,
            db_name=db_name,
            admin_password=admin_password,
            cpu_core_count=compute_count,
            data_storage_size_in_tbs=storage_tb,
            database_edition="ENTERPRISE_EDITION",
            db_version=db_version,
            license_model="LICENSE_INCLUDED",
            is_free_tier=False
        )

        response = db_client.create_autonomous_database(
            create_autonomous_database_details=create_details
        )

        BaseTool.log_call("create_oci_autonomous_database", provider="oracle", db_name=db_name)
        return f"Autonomous Database '{db_name}' criado com sucesso na OCI. OCID: {response.data.id}"
    except Exception as e:
        BaseTool.log_error("create_oci_autonomous_database", "oracle", e)
        raise CloudToolError(f"Erro ao criar Autonomous Database: {str(e)}", provider="oracle")
