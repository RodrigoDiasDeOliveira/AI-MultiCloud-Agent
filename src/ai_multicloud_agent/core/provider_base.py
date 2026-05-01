from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseCloudProvider(ABC):
    """Base class for cloud providers."""

    name: str

    @abstractmethod
    def get_tools(self) -> List[str]:
        """Return tool names exposed by this cloud provider."""
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Return a health check summary for this provider."""
        raise NotImplementedError
