from typing import Any, Optional

try:
    import keyring
except ImportError:  # pragma: no cover
    keyring = None


def validate_credentials(credentials: Any) -> bool:
    return bool(credentials)


def resolve_secret(service: str, name: str) -> Optional[str]:
    """Resolve a secret from keyring when available."""
    if keyring is None:
        return None

    try:
        return keyring.get_password(service, name)
    except Exception:
        return None
