from app.application.exceptions.auth import UserNotAuthorizedError
import inspect
from functools import wraps
from app.security.context import current_user_id

def authorize(func):

    param_names = list(inspect.signature(func).parameters.keys())

    @wraps(func)
    def wrapper(*args, **kwargs):
        caller_id = current_user_id.get()
        target_user_id = None

        # 1. Check in args for user_id 
        for name, value in zip(param_names, args):
            if name == "user_id":
                target_user_id = value
                break
        
        # 2. Check in dto (positional arguments)
        if target_user_id is None:
            for arg in args:
                if hasattr(arg, "user_id"):
                    target_user_id = getattr(arg, "user_id")
                    break
        
        # 3. Check user_id in kwards
        if target_user_id is None:
            if "user_id" in kwargs:
                target_user_id = kwargs["user_id"]

        # 4. Check in kwargs dto
        if target_user_id is None:
            for kwarg_value in kwargs.values():
                if hasattr(kwarg_value, "user_id"):
                    target_user_id = getattr(kwarg_value, "user_id")
                    break
        

        # If target_user_id not found, raise error
        if target_user_id is None:
            raise UserNotAuthorizedError("User id is not provided.")

        # 4. IDOR control
        if caller_id != target_user_id:
            raise UserNotAuthorizedError(
                "Access denied: You don't have permission to access this user (IDOR)."
            )

        return func(*args, **kwargs)
    return wrapper