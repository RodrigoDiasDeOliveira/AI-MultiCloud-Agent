from ai_multicloud_agent.tools.base import BaseTool


class AWSSecurityTool(BaseTool):
    def __init__(self) -> None:
        super().__init__("aws_security")


def aws_security_overview() -> dict[str, str]:
    return {"status": "aws security stub", "message": "Implementação de segurança AWS pendente."}
