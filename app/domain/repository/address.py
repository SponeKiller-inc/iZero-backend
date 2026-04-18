from abc import ABC, abstractmethod

from app.models.address.addresses import Addresses

class IAddressRepository(ABC):
    @abstractmethod
    def get_address(self, address_id: int) -> Addresses | None:
        pass

    @abstractmethod
    def get_all_addresses(self) -> list[Addresses] | list:
        pass
