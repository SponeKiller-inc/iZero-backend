from app.application.exceptions.person import PersonValidationError
from app.domain.shared.entities.email import Email
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.value_objects.contact import EmailAddress


def get_or_create_email(email_repository: EmailRepository, address: str | None) -> Email | None:
    """
    Get the stored e-mail with the given address, creating it when it is not stored yet.

    Args:
        email_repository: E-mail repository
        address: E-mail address, None if no e-mail

    Returns:
        The saved e-mail, None if no address is given

    Raises:
        PersonValidationError: If the address has invalid format
    """
    if not address:
        return None

    try:
        email_address = EmailAddress(address)
    except ValueError as e:
        raise PersonValidationError(str(e)) from e

    email = email_repository.get_by_address(email_address.value)

    if email is None:
        email = email_repository.save(Email.create(address=email_address))

    return email
