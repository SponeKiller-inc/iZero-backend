from datetime import date


def full_years_between(start: date, end: date) -> int:
    """
    Calculates the number of whole years elapsed from start to end, e.g. the age
    of a person from their date of birth.

    Args:
        start: The date the period starts.
        end: The date the period ends.

    Returns:
        The number of whole years; an anniversary not reached yet in the end year
        counts one year less (29 February counts as reached on 1 March in non-leap years).
    """
    anniversary_not_reached = (end.month, end.day) < (start.month, start.day)

    return end.year - start.year - anniversary_not_reached
