from app.domain.shared.exceptions.errors import DomainError


class PersonValidationError(DomainError):
    """Person details violate the person rules"""
