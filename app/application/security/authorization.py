import inspect
from functools import wraps
from app.security.context import current_user_id  # Tvůj ContextVar

def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        caller_id = current_user_id.get()
        target_user_id = None

        # 1. Zkontroluj, zda target_id není přímo v pojmenovaných argumentech (kwargs)
        if "user_id" in kwargs:
            target_user_id = kwargs["user_id"]
        
        # 2. Pokud ne, prohledej objekty v pozičních argumentech (args) - např. tvé DTO
        else:
            for arg in args:
                if hasattr(arg, "user_id"):
                    target_user_id = getattr(arg, "user_id")
                    break
                # Pokud předáváš DTO jako obyčejný dict
                elif isinstance(arg, dict) and "user_id" in arg:
                    target_user_id = arg["user_id"]
                    break

        # 3. Pokud jsi target_user_id nenašel ani v jednom, zkontroluj kwargs s DTO
        if target_user_id is None:
            for kwarg_value in kwargs.values():
                if hasattr(kwarg_value, "user_id"):
                    target_user_id = getattr(kwarg_value, "user_id")
                    break

        # Pokud jsi ID vůbec nenašel, vyhoď chybu architektury
        if target_user_id is None:
            raise AttributeError(f"Funkce {func.__name__} nemá v DTO ani parametrech 'user_id'.")

        # 4. Provedení samotné IDOR kontroly
        if caller_id != target_user_id:
            raise PermissionError("Přístup odepřen: Nemáš oprávnění pro tohoto uživatele.")

        return func(*args, **kwargs)
    return wrapper