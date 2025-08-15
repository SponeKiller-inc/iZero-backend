from fastapi import HTTPException, status, Request

async def verify_user_owns_resource(
    request: Request,
    user_id: int
) -> None:
    """Check that the current user owns the resource

    Args:
        request: FastAPI Request, expects request.state.user_id from auth middleware
        user_id: User ID from path parameter

    Raises:
        HTTPException: 403 if user is not owner
    """
    
    if (
        not hasattr(request.state, "user_id") or 
        request.state.user_id != user_id
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
