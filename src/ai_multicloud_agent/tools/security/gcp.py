from ai_multicloud_agent.tools.base import BaseTool


class GCPSecurityTool(BaseTool):
    def __init__(self) -> None:
        super().__init__("gcp_security")


def gcp_security_overview() -> dict[str, str]:
    return {"status": "gcp security stub", "message": "Implementação de segurança GCP pendente."}
