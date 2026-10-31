from app.application.exceptions.base import ApplicationError


class PersonNotFoundError(ApplicationError):
    pass

class PersonAlreadyExistsError(ApplicationError):
    """Company registration number already identifies another entrepreneur or company (BR-6)."""

class PersonTypeChangeNotAllowedError(ApplicationError):
    """Changed details belong to another person type than the person has (BR-8)."""

class PersonValidationError(ApplicationError):
    """Person details violate the person rules (format of an identifier or contact, empty name,
    age under 18, unknown title, VAT payer without VAT ID, representative who is not a natural person)."""
