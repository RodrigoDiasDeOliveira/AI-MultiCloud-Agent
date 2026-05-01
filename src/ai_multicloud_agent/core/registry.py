from importlib import import_module
import inspect
import pkgutil
from typing import Any, Iterable, List

from fastmcp import FastMCP

from ai_multicloud_agent.tools import (
    storage,
    compute,
    database,
    networking,
    iam,
    serverless,
    containers,
    monitoring,
    kubernetes,
)

CATEGORY_MODULES = [
    storage,
    compute,
    database,
    networking,
    iam,
    serverless,
    containers,
    monitoring,
    kubernetes,
]


class ToolRegistry:
    """Registry helper that discovers and registers tool modules."""

    def __init__(self, categories: Iterable[Any] | None = None):
        self.categories = list(categories) if categories is not None else CATEGORY_MODULES

    def discover_modules(self) -> List[Any]:
        modules: List[Any] = []
        for category in self.categories:
            for _, name, _ in pkgutil.iter_modules(category.__path__):
                if name.startswith("__"):
                    continue
                module_name = f"{category.__name__}.{name}"
                try:
                    module = import_module(module_name)
                except (ImportError, ModuleNotFoundError) as error:
                    print(f"⚠️  Ignorando módulo {module_name}: dependência ausente ou importação falhou ({error})")
                    continue
                except Exception as error:
                    print(f"⚠️  Erro ao carregar módulo {module_name}: {error}")
                    continue
                modules.append(module)
        return modules

    def discover_tool_functions(self) -> dict[str, list[str]]:
        tools: dict[str, list[str]] = {}
        for module in self.discover_modules():
            names = []
            for attr_name in dir(module):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(module, attr_name)
                if inspect.isfunction(attr):
                    names.append(attr_name)
            if names:
                tools[module.__name__] = names
        return tools

    def register_all_tools(self, mcp: FastMCP) -> None:
        """Discover and import all tool modules so the MCP server can register them."""
        print("🔄 Registrando tools do AI-MultiCloud-Agent MCP Server...\n")

        for module in self.discover_modules():
            module_name = module.__name__.split('.')[-1].upper()
            print(f"   ✅ Módulo carregado: {module_name}")

        print("\n🚀 MCP Server iniciado com sucesso! Todas as tools foram carregadas.\n")
