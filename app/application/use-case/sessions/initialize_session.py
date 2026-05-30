from app.domain.session.repositories.session import SessionRepository
from app.domain.users.repositories.user import UserRepository
from app.domain.users.exceptions.user import UserNotFoundError
from app.application.dto.sessions.initialize_session import InitializeSessionIn


class InitializeSession:

    def __init__(
        self,
        session_repository: SessionRepository,
        user_repository: UserRepository,
    ) -> None:
        """
        Initializes a new session.

        Args:
            session_repository (SessionRepository): The session repository.
        """
        self.session_repository = session_repository
        self.user_repository = user_repository

    def execute(self, dto: InitializeSessionIn) -> None:
        """
        Initializes a new session.

        Args:
            dto (InitializeSessionIn): The session data.
        """
        # 1. Zeptame se repository zda uživatel existuje, pokud ne končíme 
        if dto.user_id > 0:
            user_exists = self.user_repository.exists_user(dto.user_id)

            if not user_exists:
                raise UserNotFoundError
        

        session = self.session 
        
        
        

        # Pokud neexistujem vracíme chybu usernotfound
        # 2. vytvoříme entitu session
        # 3. zalogujeme entitu session 


        