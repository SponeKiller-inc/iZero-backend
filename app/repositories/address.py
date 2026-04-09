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
    
    def get_country_code(self, address_id: int) -> Addresses | None:
        """
        Retrieve country code

        Args:
            address_id (int): address id

        Returns:
            Addresses or None:  country code or None if no country code found
        """

        return (
            self.db
                .query(Addresses)
                .filter(
                    Addresses.id == address_id
                )
                .first()
        )
    
    def get_available_country(
        self,
        country_code: str
    ) -> AddressRegistry | None:
        """
        Provides proper repository function to get address data
        Args:
            country_code (str): country code

        Returns:
            AddressRegistry or None:  available country 
                or None if no available country found
        """
        
        return (
            self.db
                .query(AddressRegistry)
                .filter(
                    AddressRegistry.country_code == country_code,
                    AddressRegistry.valid_at(get_UTC_current_time())
                )
                .first()
        )
     
    def get_all_available_countries(self) -> list[AddressRegistry] | []:
        """
        Get all available countries and proper repository function
        to get address data

        Returns:
            list[AddressRegistry] or []:  list of available countries 
                or empty list if no available countries found
        """
        
        return (
            self.db
                .query(AddressRegistry)
                .filter(AddressRegistry.valid_at(get_UTC_current_time()))
                .all()
        )
     
    def get_all_available_countries(self) -> list[AddressRegistry] | []:
        """
        Get all available countries

        Returns:
            list[AddressRegistry] or []:  list of available countries 
                or empty list if no available countries found
        """
        
        return (
            self.db
                .query(AddressRegistry)
                .filter(AddressRegistry.valid_at(get_UTC_current_time()))
                .all()
        )
    
