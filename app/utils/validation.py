from typing import Any

def validate_positive_int(name: str, value: Any) -> None:
    """
    Validate dtype int and value greater than zero

    Raises:
        TypeError:   if `value` not int
        ValueError:  if `value` <= 0
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be > 0, got {value}")


def validate_non_empty_str(name: str, value: Any) -> None:
    """
    Validate dtype str and value not empty

    Raises:
        TypeError:   if `value` not str
        ValueError:  if `value` is not empty
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str, got {type(value).__name__}")
    if value == "":
        raise ValueError(f"{name} must not be empty")
