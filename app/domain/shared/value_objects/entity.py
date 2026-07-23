from dataclasses import dataclass

from app.domain.shared.constants.entity_type import EntityType

@dataclass(frozen=True)
class Entity:
    """
    Represents the entity.

    Attributes:
        type: The type of the entity.
    """
    type: EntityType