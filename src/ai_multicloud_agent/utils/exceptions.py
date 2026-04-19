# src/ai_multicloud_agent/utils/exceptions.py

class CloudToolError(Exception):
    """Exceção base para erros nas tools de cloud."""
    def __init__(self, message: str, provider: str = None, operation: str = None):
        self.provider = provider
        self.operation = operation
        super().__init__(message)

class AuthenticationError(CloudToolError):
    """Erro de autenticação ou credenciais inválidas."""
    pass

class ResourceNotFoundError(CloudToolError):
    """Quando um recurso (bucket, VM, database, etc.) não é encontrado."""
    pass

class PermissionError(CloudToolError):
    """Falta de permissão para executar a operação."""
    pass

class ValidationError(CloudToolError):
    """Erro de validação de parâmetros."""
    pass