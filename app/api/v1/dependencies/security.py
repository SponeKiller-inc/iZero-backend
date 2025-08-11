from fastapi import HTTPException, status, Request

async def verify_user_owns_resource(
    request: Request
) -> None:
    user_id = request.path_params.get("user_id")
    
    if user_id is None:
        # No check if not in path parm
        return
    
    if (
        not hasattr(request.state.user_id) or 
        request.state.user_id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
