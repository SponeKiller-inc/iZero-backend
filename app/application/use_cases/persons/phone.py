from app.application.exceptions.person import PersonValidationError
from app.domain.shared.entities.phone import Phone
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository
from app.domain.shared.value_objects.contact import PhoneNumber


def get_or_create_phone(
    phone_prefix_repository: PhonePrefixRepository,
    phone_repository: PhoneRepository,
    phone_prefix_id: int | None,
    phone_number: str | None,
) -> Phone | None:
    """
    Get the stored phone with the given calling code and national number, creating it
    when it is not stored yet.

    Args:
        phone_prefix_repository: Phone prefix repository
        phone_repository: Phone repository
        phone_prefix_id: ID of the calling code from the catalogue, None if no phone
        phone_number: National phone number, None if no phone

    Returns:
        The saved phone, None if neither the calling code nor the number is given

    Raises:
        PersonValidationError: If only one of calling code and number is given, the
            calling code does not exist or the number is not a Czech 9-digit number
    """
    if phone_prefix_id is None and not phone_number:
        return None

    if phone_prefix_id is None or not phone_number:
        raise PersonValidationError("Phone needs both a calling code and a number")

    phone_prefix = phone_prefix_repository.get(phone_prefix_id)

    if phone_prefix is None:
        raise PersonValidationError("Phone prefix does not exist")

    try:
        number = PhoneNumber(phone_number)
    except ValueError as e:
        raise PersonValidationError(str(e)) from e

    phone = phone_repository.get_by_number(phone_prefix.id, number.value)

    if phone is None:
        phone = phone_repository.save(Phone.create(prefix=phone_prefix, number=number))

    return phone
