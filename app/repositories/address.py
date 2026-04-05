from datetime import datetime

from sqlalchemy.orm import Session

from app.utils.utils import get_UTC_current_time
from app.models.address.czech_addresses import CzechAddresses
from app.models.address.addresses import Addresses
from app.models.address.address_registry import AddressRegistry



class AddressRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_czech_address(self, address_id: int) -> CzechAddresses | None:
        """
        Retrieve czech address

        Args:
            address_id (int): address id

        Returns:
            CzechAddresses or None:  czech address or None if no czech address found
        """

        return (
            self.db
                .query(CzechAddresses)
                .filter(
                    CzechAddresses.id == address_id
                )
                .first()
        )   

    def get_all_czech_addresses(self) -> list[CzechAddresses] | []:
        """
        Get all czech addresses

        Returns:
            list[CzechAddresses] or []:  list of czech addresses 
                or empty list if no czech addresses found
        """
        
        return (
            self.db
                .query(CzechAddresses)
                .all()
        )
    
    def get_country_code(self, country_code: str) -> Addresses | None:
        """
        Retrieve country code

        Args:
            country_code (str): country code - ISO 3-alpha code (e.g. "CZE")

        Returns:
            CzechAddresses or None:  czech address or None if no czech address found
        """

        return (
            self.db
                .query(CzechAddresses)
                .filter(
                    CzechAddresses.country_code == country_code
                )
                .first()
        )
     
    def get_available_countries(
        self, 
        ref_date: datetime = get_UTC_current_time()
    ) -> list[AddressRegistry] | []:
        """
        Get all available countries

        Args:
            ref_date (datetime): reference date (default: current UTC datetime)

        Returns:
            list[AddressRegistry] or []:  list of available countries 
                or empty list if no available countries found
        """
        
        return (
            self.db
                .query(AddressRegistry)
                .filter(AddressRegistry.valid_at(ref_date))
                .all()
        )