from ai_multicloud_agent.tools.base import BaseTool


class OracleSecurityTool(BaseTool):
    def __init__(self) -> None:
        super().__init__("oracle_security")


def oracle_security_overview() -> dict[str, str]:
    return {"status": "oracle security stub", "message": "Implementação de segurança Oracle OCI pendente."}
