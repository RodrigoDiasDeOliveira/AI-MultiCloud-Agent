import importlib
import pkgutil
from fastapi import FastAPI


def register_tools(app: FastAPI) -> None:
    package = "ai_multicloud_agent.tools"
    for importer, modname, ispkg in pkgutil.walk_packages(
        importlib.import_module(package).__path__, package + "."
    ):
        if modname.endswith(".__init__"):
            continue
        module = importlib.import_module(modname)
        if hasattr(module, "register"):
            module.register(app)
