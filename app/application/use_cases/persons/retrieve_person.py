from app.application.constants.use_case import UseCase
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import PersonNotFoundError
from app.application.security.authorize import authorize
from app.application.use_cases.persons.retrieve_company import RetrieveCompany
from app.application.use_cases.persons.retrieve_entrepreneur import RetrieveEntrepreneur
from app.application.use_cases.persons.retrieve_natural_person import (
    RetrieveNaturalPerson,
)
from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.repositories.person import PersonRepository
from app.domain.shared.constants.entity_type import EntityType


class RetrievePerson:

    def __init__(
        self,
        person_repository: PersonRepository,
        retrieve_natural_person: RetrieveNaturalPerson,
        retrieve_entrepreneur: RetrieveEntrepreneur,
        retrieve_company: RetrieveCompany,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            retrieve_natural_person: Retrieve natural person use-case
            retrieve_entrepreneur: Retrieve entrepreneur use-case
            retrieve_company: Retrieve company use-case
        """
        self.person_repository = person_repository
        self.retrieve_natural_person = retrieve_natural_person
        self.retrieve_entrepreneur = retrieve_entrepreneur
        self.retrieve_company = retrieve_company

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE)
    def execute(self, person_id: int) -> PersonOut:
        """
        Retrieve a person with the details of its type

        Args:
            person_id: Person ID

        Returns:
            The person with the details of its type

        Raises:
            PersonNotFoundError: If the person or its type-specific details do not exist
        """
        person = self.person_repository.get(person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        match person.person_type:
            case PersonType.NATURAL_PERSON:
                return PersonOut(
                    id=person.id,
                    person_type=person.person_type.value,
                    natural_person=self.retrieve_natural_person.execute(person.id),
                )
            case PersonType.ENTREPRENEUR:
                return PersonOut(
                    id=person.id,
                    person_type=person.person_type.value,
                    entrepreneur=self.retrieve_entrepreneur.execute(person.id),
                )
            case PersonType.COMPANY:
                return PersonOut(
                    id=person.id,
                    person_type=person.person_type.value,
                    company=self.retrieve_company.execute(person.id),
                )
