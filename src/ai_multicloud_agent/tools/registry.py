# src/ai_multicloud_agent/tools/registry.py

from fastmcp import FastMCP
import importlib
import pkgutil

# Importa todos os módulos de tools
from ai_multicloud_agent.tools import (
    storage,
    compute,
    database,
    networking,
    iam,
    serverless,
    containers,
    monitoring,
    kubernetes
)

def register_all_tools(mcp: FastMCP):
    """Registra automaticamente todas as tools do AI-MultiCloud-Agent."""
    modules = [
        storage, compute, database, networking, iam, 
        serverless, containers, monitoring, kubernetes
    ]

    print("🔄 Registrando tools do AI-MultiCloud-Agent MCP Server...\n")

    for module in modules:
        module_name = module.__name__.split('.')[-1].upper()
        registered = 0
        for _, name, _ in pkgutil.iter_modules(module.__path__):
            if name.startswith("__"):
                continue
            full_name = f"{module.__name__}.{name}"
            try:
                importlib.import_module(full_name)
                registered += 1
            except Exception as e:
                print(f"   ❌ Erro ao importar {module_name}/{name}: {e}")

        print(f"   ✅ {module_name:<12} → {registered} tools registradas")

    print("\n🚀 MCP Server iniciado com sucesso! Todas as tools foram carregadas.\n")