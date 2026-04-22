from sqlalchemy.orm import Session

from app.models.address import Addresses



class AddressRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_address(self, address_id: int) -> Addresses | None:
        """
        Retrieve address

        Args:
            address_id (int): address id

        Returns:
            Addresses or None:  address or None if no address found
        """

        return (
            self.db
                .query(Addresses)
                .filter(
                    Addresses.id == address_id
                )
                .first()
        )   

    def get_all_addresses(self) -> list[Addresses] | []:
        """
        Get all addresses

        Returns:
            list[Addresses] or []:  list of addresses 
                or empty list if no addresses found
        """
        
        return (
            self.db
                .query(Addresses)
                .all()
        )