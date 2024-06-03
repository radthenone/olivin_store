from abc import ABC, abstractmethod
from typing import Any, Optional


class IRegistrationEmailHandler(ABC):
    @abstractmethod
    def send_registration_email(
        self,
        to_email: str,
        context: Optional[dict[str, Any]] = None,
    ) -> bool:
        pass
