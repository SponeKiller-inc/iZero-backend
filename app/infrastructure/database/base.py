from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import DateTime, MetaData, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, composite

from app.domain.shared.value_objects.period import ValidityPeriod
from app.infrastructure.services.time_provider import SystemTimeProvider

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

    validity: Mapped[ValidityPeriod] = composite(
        ValidityPeriod, 
        valid_from, 
        valid_to
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
        default=lambda: SystemTimeProvider.now(),
        sort_order=998,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: SystemTimeProvider.now(),
        onupdate=lambda: SystemTimeProvider.now(),
        sort_order=999,
    )

class Base(TimestampMixin, DeclarativeBase):
    """
    Base class for all ORM models, combining timestamp fields and shared metadata.

    Inherits:
        TimestampMixin: adds created_at and updated_at timestamps to all models.
        DeclarativeBase: SQLAlchemy declarative base.

    Attributes:
        metadata (MetaData): SQLAlchemy MetaData object for defining table schemas.
    """
    metadata = MetaData()


