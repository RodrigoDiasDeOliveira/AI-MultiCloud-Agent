from google.cloud import functions_v2
from fastmcp import tool
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.base import BaseTool
from ai_multicloud_agent.utils.exceptions import CloudToolError
import os

@tool
def list_gcp_cloud_functions() -> dict:
    """Lista Cloud Functions no GCP."""
    try:
        if settings.gcp.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp.credentials_path

        client = functions_v2.FunctionServiceClient()
        parent = f"projects/{settings.gcp.project_id}/locations/-"
        response = client.list_functions(parent=parent)

        functions = [f.name.split('/')[-1] for f in response]
        BaseTool.log_call("list_gcp_cloud_functions", provider="gcp", count=len(functions))
        return {"functions": functions, "count": len(functions)}
    except Exception as e:
        BaseTool.log_error("list_gcp_cloud_functions", "gcp", e)
        raise CloudToolError(f"Erro ao listar Cloud Functions: {str(e)}", provider="gcp")