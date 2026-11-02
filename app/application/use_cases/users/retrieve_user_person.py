from app.application.constants.use_case import UseCase
from app.application.dto.person.person import PersonOut
from app.application.security.authorize import authorize
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.repositories.user_person import UserPersonRepository


class RetrieveUserPerson:

    def __init__(
        self,
        user_person_repository: UserPersonRepository,
        retrieve_person: RetrievePerson,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_person_repository: User person repository
            retrieve_person: Retrieve person use-case
        """
        self.user_person_repository = user_person_repository
        self.retrieve_person = retrieve_person

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE_USER_PERSON)
    def execute(self, user_id: int) -> PersonOut | None:
        """
        Retrieve the user's person with the details of its type

        Args:
            user_id: User ID

        Returns:
            The user's person, None if user has no person

        Raises:
            PersonNotFoundError: If the assigned person or its details do not exist
        """
        user_person = self.user_person_repository.get_by_user_id(user_id)

        if user_person is None:
            return None

        return self.retrieve_person.execute(user_person.person_id)
