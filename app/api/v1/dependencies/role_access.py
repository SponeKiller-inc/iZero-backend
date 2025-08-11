from fastapi import Depends, Request, HTTPException, status

from .user import UserDependencies
from app.services.user import UserService
from app.exceptions.domain.user import UserRoleNotFoundError
from app.exceptions.infrastucture.domain import UserServiceError


def require_role(allowed_role: str) -> None:
    """
    Dependency to enforce that the current user has the specified role.

    Example Usage in a router:
        @router.get("/admin", dependencies=[require_roles("admin")])
        async def admin_endpoint():
            ...
    Args:
        allowed_role (str) - which role is allowed to access resources
    
    Raises:
        HTTPException:
            If user does not have required role (403) 
            if user role has not been found (404)
            if there was an server error while retrieving user role (500)
    """
    async def dependency(
        request: Request,
        user_service: UserService = Depends(UserDependencies),
    ) -> None:
        try:
            user_role = user_service.retrieve_user_role(request.state.user_id)
        except UserRoleNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Access denied, user role not found"
            )
        except UserServiceError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "Something went wrong while checking access role, "
                    "please try again later."
                ),
            )

        if user_role != allowed_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access allowed only to role: {allowed_role}"
            )
    return Depends(dependency)
