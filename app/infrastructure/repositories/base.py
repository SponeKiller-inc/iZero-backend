from sqlalchemy import func, select
from sqlalchemy.orm import Session


class BaseAlchemyRepository:
    def __init__(self, db: Session):
        self.db = db

    def _resync_sequence(self, table: str, column: str, value: int) -> None:
        """
        Re-sync a serial/identity column's sequence after an explicit-ID insert,
        so a later auto-generated ID doesn't collide with it.

        Args:
            table (str): table name
            column (str): serial/identity column name
            value (int): the explicit ID just inserted
        """

        self.db.execute(select(func.setval(func.pg_get_serial_sequence(table, column), value)))