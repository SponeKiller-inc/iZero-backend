from app.application.ports.time_provider import TimeProvider
from app.domain.session.entities.session import Session
from app.domain.session.repositories.session import SessionRepository
from app.domain.users.repositories.user import UserRepository
from app.domain.users.exceptions.user import UserNotFoundError
from app.application.dto.sessions.initialize_session import InitializeSessionIn


class InitializeSession:

    def __init__(
        self,
        session_repository: SessionRepository,
        user_repository: UserRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initializes a new session.

        Args:
            session_repository (SessionRepository): The session repository.
        """
        self.session_repository = session_repository
        self.user_repository = user_repository
        self.time_provider = time_provider

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
        

        # 2. Ověříme  zda external_id není nulovéé, pokud není tak  zkusíme test platnosti
        # pokud projde, vracíme se

        if dto.external_id > 0:
            session = self.session_repository.get_by_external_id(dto.external_id)

            if session and not session.is_expired(self.time_provider.now()):
                return

        # 3. Pokud uživatel je nenulový tak zneplatníme všechny aktivní session
        if dto.user_id > 0:
            last_session = self.session_repository.get_last_user_session(dto.user_id)
        
            

        # 4. Vytvoříme instanci nové session

        # 5. uložíme do DB

        # 6. Vracíme se 



        session = Session.create_new()
        