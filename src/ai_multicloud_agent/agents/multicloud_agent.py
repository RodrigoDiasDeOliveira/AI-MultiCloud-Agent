# src/ai_multicloud_agent/agents/multicloud_agent.py

from typing import Dict, Any
import structlog
from rich.console import Console

from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.mcp.server import mcp

console = Console()
logger = structlog.get_logger()

class MultiCloudAgent:
    """
    Agente conversacional em português que utiliza o MCP Server
    para gerenciar infraestrutura multi-cloud de forma inteligente.
    """

    def __init__(self):
        self.name = "MultiCloud Assistant"
        self.description = "Agente especialista em AWS, Azure, GCP e Oracle OCI"

    async def chat(self, user_message: str) -> str:
        """
        Método principal: recebe mensagem do usuário em português
        e retorna resposta + ações executadas via MCP.
        """
        console.print(f"\n[bold cyan]👤 Usuário:[/bold cyan] {user_message}")

        try:
            # Aqui o agente envia a mensagem para o MCP Server via search-and-execute
            # Em produção, isso seria feito através de um cliente MCP ou LangGraph
            logger.info("agent_query", message=user_message)

            # Exemplo de resposta inteligente (pode ser expandido com LangGraph/CrewAI)
            response = self._process_query(user_message)

            console.print(f"[bold green]🤖 {self.name}:[/bold green] {response}")
            return response

        except Exception as e:
            logger.error("agent_error", error=str(e))
            error_msg = f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            return error_msg

    def _process_query(self, message: str) -> str:
        """Lógica simples de processamento (pode ser substituída por LLM + tools)."""
        message_lower = message.lower()

        if any(word in message_lower for word in ["criar", "criar um", "provisionar", "deploy"]):
            if "bucket" in message_lower or "storage" in message_lower:
                return "✅ Entendido! Vou criar um bucket de storage. Qual cloud você prefere (AWS, Azure, GCP ou OCI) e qual o nome do bucket?"

            elif "vm" in message_lower or "instância" in message_lower or "servidor" in message_lower:
                return "🚀 Entendido! Vou criar uma máquina virtual. Qual o tipo (t3.micro, Standard_B1s, etc.) e em qual região/cloud?"

            elif "postgresql" in message_lower or "banco" in message_lower or "database" in message_lower:
                return "🗄️ Entendido! Vou criar uma instância PostgreSQL. Qual cloud e qual nome do banco?"

        elif any(word in message_lower for word in ["listar", "mostrar", "ver"]):
            if "bucket" in message_lower:
                return "📋 Vou listar todos os buckets disponíveis. Aguarde enquanto consulto as clouds..."
            elif "vm" in message_lower or "instância" in message_lower:
                return "📋 Listando todas as máquinas virtuais ativas..."

        # Resposta padrão
        return (
            "Entendi sua solicitação! Como sou um agente multi-cloud, posso ajudar com:\n"
            "• Criar e gerenciar storage, VMs, bancos de dados\n"
            "• Configurar redes, IAM, serverless e containers\n"
            "• Monitoramento e Kubernetes\n\n"
            "Pode ser mais específico? Ex: 'Crie um bucket S3 chamado meus-backups na região us-east-1'"
        )


# Instância global do agente
multi_cloud_agent = MultiCloudAgent()


# Função helper para uso direto
async def run_agent_demo():
    """Demo interativo simples para testar o agente."""
    console.print(Panel.fit(
        "[bold cyan]🤖 MultiCloud Agent Demo[/bold cyan]\n"
        "Digite 'sair' para encerrar.",
        border_style="cyan"
    ))

    while True:
        try:
            user_input = input("\n[bold]Você:[/bold] ").strip()
            if user_input.lower() in ["sair", "exit", "quit"]:
                console.print("[yellow]👋 Encerrando agente...[/yellow]")
                break
            await multi_cloud_agent.chat(user_input)
        except KeyboardInterrupt:
            break