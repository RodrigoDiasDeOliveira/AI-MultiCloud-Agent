from fastapi import FastAPI
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import sys
from typing import Optional

from ai_multicloud_agent.mcp.server import mcp
from ai_multicloud_agent.config.settings import settings
from ai_multicloud_agent.tools.registry import register_all_tools

console = Console()
cli = typer.Typer(
    name="ai-multicloud-agent",
    help="🚀 AI-MultiCloud-Agent - MCP Server para gerenciamento multi-cloud",
    add_completion=True,
    rich_markup_mode="rich"
)

app = FastAPI(title="AI-MultiCloud-Agent API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}

@cli.command()
def run(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host para rodar o servidor"),
    port: int = typer.Option(8000, "--port", "-p", help="Porta do servidor MCP"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Modo verbose (mais logs)")
):
    """Inicia o MCP Server com todas as tools registradas."""
    
    if verbose:
        settings.log_level = "DEBUG"

    console.print(Panel.fit(
        "[bold cyan]AI-MultiCloud-Agent[/bold cyan] [dim]— MCP Server v0.1.0[/dim]\n"
        "Gerenciamento completo de infraestrutura em AWS, Azure, GCP e Oracle OCI",
        title="🚀 Iniciando Servidor",
        border_style="cyan"
    ))

    # Registra todas as tools antes de iniciar
    register_all_tools(mcp)

    rprint(f"\n[green]✅ Servidor MCP rodando em:[/green] http://{host}:{port}")
    rprint("[yellow]📡 Agentes de IA podem se conectar via Model Context Protocol[/yellow]\n")

    try:
        mcp.run(host=host, port=port)
    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Servidor encerrado pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Erro fatal: {e}[/red]")
        sys.exit(1)


@cli.command()
def tools(
    category: Optional[str] = typer.Argument(
        None, 
        help="Filtrar por categoria (storage, compute, database, networking, iam, serverless, containers, monitoring, kubernetes)"
    )
):
    """Lista todas as tools disponíveis ou filtra por categoria."""
    console.print(Panel.fit(
        "[bold]Ferramentas Disponíveis no MCP Server[/bold]",
        border_style="blue"
    ))

    # Aqui poderíamos fazer uma introspecção mais avançada no futuro
    # Por enquanto, mostramos as categorias registradas
    categories = {
        "storage": "Object Storage, Buckets, Upload/Download",
        "compute": "VMs, Instances, Scaling",
        "database": "RDS, PostgreSQL, Cloud SQL, Autonomous DB",
        "networking": "VPC, VNet, Security Groups, Firewalls",
        "iam": "Users, Roles, Policies, Service Accounts",
        "serverless": "Lambda, Azure Functions, Cloud Functions",
        "containers": "ECS, AKS, GKE, OKE",
        "monitoring": "Alarmes, Alertas, CloudWatch, Monitor",
        "kubernetes": "EKS, AKS, GKE, OKE"
    }

    table = Table(title="Categorias de Tools", show_header=True, header_style="bold cyan")
    table.add_column("Categoria", style="green")
    table.add_column("Descrição", style="dim")

    if category:
        cat_lower = category.lower()
        if cat_lower in categories:
            table.add_row(cat_lower.upper(), categories[cat_lower])
            console.print(table)
            rprint(f"\n[bold green]Use o agente de IA para explorar as tools de {cat_lower.upper()}.[/bold green]")
        else:
            rprint(f"[red]Categoria '{category}' não encontrada.[/red]")
            rprint(f"Categorias disponíveis: {', '.join(categories.keys())}")
    else:
        for cat, desc in categories.items():
            table.add_row(cat.upper(), desc)
        console.print(table)
        rprint("\n[italic]Dica:[/italic] Use [bold]ai-multicloud-agent tools <categoria>[/bold] para mais detalhes.")


@cli.command()
def status():
    """Mostra o status atual da configuração e clouds conectadas."""
    console.print(Panel.fit(
        "[bold cyan]Status do AI-MultiCloud-Agent[/bold cyan]",
        border_style="cyan"
    ))

    table = Table(show_header=True, header_style="bold")
    table.add_column("Configuração", style="cyan")
    table.add_column("Status", style="green")

    table.add_row("MCP Server Name", settings.mcp_server_name)
    table.add_row("Log Level", settings.log_level)

    # Verifica quais clouds têm credenciais básicas configuradas
    clouds = []
    if settings.aws.access_key_id and settings.aws.secret_access_key:
        clouds.append("AWS ✅")
    if settings.azure.subscription_id and settings.azure.client_id:
        clouds.append("Azure ✅")
    if settings.gcp.project_id:
        clouds.append("GCP ✅")
    if settings.oracle.compartment_id and settings.oracle.namespace:
        clouds.append("Oracle OCI ✅")

    table.add_row("Clouds Configuradas", "\n".join(clouds) if clouds else "Nenhuma (configure no .env)")

    console.print(table)


@cli.command()
def version():
    """Mostra a versão do projeto."""
    rprint("[bold cyan]AI-MultiCloud-Agent[/bold cyan] [dim]v0.1.0[/dim]")
    rprint("MCP Server para AI Agents gerenciarem infraestrutura multi-cloud")


if __name__ == "__main__":
    cli()