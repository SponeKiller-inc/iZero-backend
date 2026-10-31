from app.domain.shared.entities.email import Email
from app.domain.shared.value_objects.contact import EmailAddress
from app.infrastructure.models.contact.emails import EmailModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyEmailRepository(BaseAlchemyRepository):
    def get(self, email_id: int) -> Email | None:
        """
        Get e-mail by ID

        Args:
            email_id: E-mail ID

        Returns:
            Email entity if found, else None
        """

        email_model = (
            self.db
                .query(EmailModel)
                .filter(EmailModel.id == email_id)
                .first()
        )

        if email_model is None:
            return None

        return self._to_entity(email_model)

    def get_by_address(self, address: str) -> Email | None:
        """
        Get e-mail by its address

        Args:
            address: E-mail address

        Returns:
            Email entity if found, else None
        """

        email_model = (
            self.db
                .query(EmailModel)
                .filter(EmailModel.address == address)
                .first()
        )

        if email_model is None:
            return None

        return self._to_entity(email_model)

    def save(self, email: Email) -> Email:
        """
        Save new e-mail; a stored e-mail is shared by every record using it and cannot
        be changed, so an existing one is returned unchanged

        Args:
            email: Email entity to save

        Returns:
            Saved e-mail entity
        """

        if email.id is None:
            return self._insert(email)

        return email

    def _insert(self, email: Email) -> Email:
        email_model = EmailModel(address=email.address.value)
        self.db.add(email_model)
        self.db.flush()
        self.db.refresh(email_model)

        return self._to_entity(email_model)

    @staticmethod
    def _to_entity(email_model: EmailModel) -> Email:
        return Email(id=email_model.id, address=EmailAddress(email_model.address))
