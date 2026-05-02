from abc import ABC, abstractmethod

from app.domain.entity.address import Address

class IAddressRepository(ABC):
    @abstractmethod
    def get_address(self, address_id: int) -> Address | None:
        pass

    @abstractmethod
    def get_all_addresses(self) -> list[Address] | list:
        pass
