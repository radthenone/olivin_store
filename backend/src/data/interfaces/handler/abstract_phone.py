from abc import ABC, abstractmethod
from typing import Optional


class IPhoneHandler(ABC):
    @abstractmethod
    def send_sms(
        self,
        number: str,
        message: str,
        title: str = "Olivin Store",
        **kwargs,
    ) -> bool:
        pass

    @abstractmethod
    def verify_number(
        self,
        number: str,
        brand: str,
        **kwargs,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def verify_number_code(
        self,
        request_id: str,
        code: str,
        **kwargs,
    ) -> bool:
        pass
