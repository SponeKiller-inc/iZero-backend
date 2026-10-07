from app.application.exceptions.base import ApplicationError


class AddressNotFoundError(ApplicationError):
    pass


class AddressProviderError(ApplicationError):
    """Specific error indicating that the external address provider has failed."""
