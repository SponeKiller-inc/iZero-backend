from datetime import datetime, timezone
from typing import Union

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy import DateTime, MetaData

from app.utils.utils import get_UTC_current_time

class ValidityMixin:
    """
    Mixin for adding validity fields to models
    """
    valid_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        sort_order=996,
    )
    valid_to: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        sort_order=997,
    )

    @classmethod
    def valid_at(cls, ref_date: datetime):
        """Returns a filter for the record valid at a specific point in time."""
        return (cls.valid_from <= ref_date) & (cls.valid_to > ref_date)

    @declared_attr
    def __table_args__(cls):
        return (
            CheckConstraint(
                cls.valid_to > cls.valid_from,
                # Dynamický název podle jména tabulky
                name=f"ck_{cls.__tablename__}_valid_dates"
            ),
        )

class TimestampMixin:
    """
    Mixin for adding timestamp fields to models
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        sort_order=998,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        sort_order=999,
    )

class CurrentMixin:
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

class Base(TimestampMixin, CurrentMixin, DeclarativeBase):
    """
    Base class for all ORM models, combining timestamp fields and shared metadata.

    Inherits:
        TimestampMixin: adds created_at and updated_at timestamps to all models.
        DeclarativeBase: SQLAlchemy declarative base.

    Attributes:
        metadata (MetaData): SQLAlchemy MetaData object for defining table schemas.
    """
    metadata = MetaData()


