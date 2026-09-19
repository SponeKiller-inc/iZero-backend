from app.domain.auth.entities.refresh_token import RefreshToken
from app.infrastructure.models.auth.refresh_token import RefreshTokenModel
from app.infrastructure.repositories.base import BaseAlchemyRepository

class AlchemyRefreshTokenRepository(BaseAlchemyRepository):

    def get_by_session_id(self, session_id: int) -> RefreshToken | None:
        """
        Retrieve refresh token by session id

        Args:
            session_id (int): session id

        Returns:
            RefreshToken or None: refresh token data or None if no data present
        """
        refresh_token_model = (
            self.db
                .query(RefreshTokenModel)
                .filter(RefreshTokenModel.session_id == session_id)
                .first()
        )

        if refresh_token_model is None:
            return None

        return self._to_entity(refresh_token_model)

    def save(self, refresh_token: RefreshToken) -> RefreshToken:
        """
        Create refresh token

        Args:
            refresh_token (RefreshToken): data to create refresh token

        Returns:
            RefreshToken: data newly created refresh token
        """
        refresh_token_model = RefreshTokenModel(
            session_id=refresh_token.session_id,
            token=refresh_token.token,
            validity=refresh_token.validity,
        )
        self.db.add(refresh_token_model)
        self.db.flush()
        self.db.refresh(refresh_token_model)

        return self._to_entity(refresh_token_model)

    def _to_entity(self, refresh_token_model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=refresh_token_model.id,
            session_id=refresh_token_model.session_id,
            token=refresh_token_model.token,
            validity=refresh_token_model.validity,
        )
