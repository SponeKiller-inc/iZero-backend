from datetime import datetime, timezone
from typing import Union

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy import DateTime, MetaData

from app.utils.utils import get_UTC_current_time

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

class ValidityMixin:
    @hybrid_method
    def is_current(cls, at: datetime = None) -> Union[BooleanClauseList, bool]:
        """
        Determine if this record is valid at a given point in time.

        When used on the model class in a query context, returns a SQL expression
        filtering rows whose valid_from ≤ at ≤ valid_to. When called on an
        instance, returns a Python bool indicating whether that instance is currently valid.

        Args:
            at (datetime, optional): The point in time to check. If None, uses the
                current UTC time via get_UTC_current_time().

        Returns:
            Union[sqlalchemy.sql.elements.BooleanClauseList, bool]:
                - In query context: a SQLAlchemy Boolean expression for use in filters.
                - In instance context: True if valid_from ≤ at ≤ valid_to, else False.
        """
        now = at or get_UTC_current_time()
        return (cls.valid_from <= now) & (cls.valid_to >= now)

class Base(TimestampMixin, ValidityMixin, DeclarativeBase):
    """
    Base class for all ORM models, combining timestamp fields and shared metadata.

    Inherits:
        TimestampMixin: adds created_at and updated_at timestamps to all models.
        DeclarativeBase: SQLAlchemy declarative base.

    Attributes:
        metadata (MetaData): SQLAlchemy MetaData object for defining table schemas.
    """
    metadata = MetaData()


