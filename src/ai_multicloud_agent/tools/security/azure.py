from ai_multicloud_agent.tools.base import BaseTool


class AzureSecurityTool(BaseTool):
    def __init__(self) -> None:
        super().__init__("azure_security")


def azure_security_overview() -> dict[str, str]:
    return {"status": "azure security stub", "message": "Implementação de segurança Azure pendente."}
