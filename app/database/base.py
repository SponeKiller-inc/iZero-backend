from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, MetaData
from datetime import datetime, timezone

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


