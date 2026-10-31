from datetime import date, datetime
from typing import Self

from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.person import Person
from app.domain.persons.exceptions.person import PersonValidationError
from app.domain.shared.services.time_span import full_years_between


class NaturalPerson:
    """
    Represents the details of a natural person (private individual).

    Attributes:
        id: The natural person ID.
        person_id: The ID of the person these details belong to.
        first_name: The first name.
        last_name: The last name.
        date_of_birth: The date of birth.
        phone_id: The ID of the phone, if known.
        email_id: The ID of the e-mail, if known.
    """

    MIN_AGE = 18

    def __init__(
        self,
        id: int | None,
        person_id: int,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        phone_id: int | None,
        email_id: int | None,
    ):
        self.id = id
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone_id = phone_id
        self.email_id = email_id

    @classmethod
    def create(
        cls,
        person: Person,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        phone_id: int | None,
        email_id: int | None,
        current_time: datetime,
    ) -> Self:
        """
        Creates the details of a natural person.

        Args:
            person: The person these details belong to.
            first_name: The first name.
            last_name: The last name.
            date_of_birth: The date of birth.
            phone_id: The ID of the phone, if known.
            email_id: The ID of the e-mail, if known.
            current_time: The current time.

        Returns:
            The newly created natural person.

        Raises:
            PersonValidationError: If the person is not a natural person, a name is
                empty/blank or the person is younger than 18.
        """
        cls._validate(person, first_name, last_name, date_of_birth, current_time)

        return cls(
            id=None,
            person_id=person.id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_id=phone_id,
            email_id=email_id,
        )

    def update(
        self,
        person: Person,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        phone_id: int | None,
        email_id: int | None,
        current_time: datetime,
    ) -> None:
        """
        Updates the details of the natural person.

        Args:
            person: The person these details belong to.
            first_name: The first name.
            last_name: The last name.
            date_of_birth: The date of birth.
            phone_id: The ID of the phone, if known.
            email_id: The ID of the e-mail, if known.
            current_time: The current time.

        Raises:
            PersonValidationError: If the person is not a natural person, a name is
                empty/blank or the person is younger than 18.
        """
        self._validate(person, first_name, last_name, date_of_birth, current_time)

        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone_id = phone_id
        self.email_id = email_id

    @classmethod
    def _validate(
        cls,
        person: Person,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        current_time: datetime,
    ) -> None:
        """
        Validates the fields shared by `create` and `update`.

        Raises:
            PersonValidationError: If the person is not a natural person (BR-2), a name
                is empty/blank or the person is younger than 18 (BR-9).
        """
        if person.person_type != PersonType.NATURAL_PERSON:
            raise PersonValidationError("Person is not a natural person.")
        if not first_name or not first_name.strip():
            raise PersonValidationError("Natural person's first name must be a non-empty string.")
        if not last_name or not last_name.strip():
            raise PersonValidationError("Natural person's last name must be a non-empty string.")

        if full_years_between(date_of_birth, current_time.date()) < cls.MIN_AGE:
            raise PersonValidationError(f"Natural person must be at least {cls.MIN_AGE} years old.")
