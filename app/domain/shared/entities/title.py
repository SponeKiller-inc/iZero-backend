class Title:
    """
    Represents the title-type entity (prefix/suffix), referenced by prefix_titles/suffix_titles.

    Attributes:
        id: The title ID.
        title_type: The type of the title ("prefix" or "suffix").
    """

    ALLOWED_TYPES = ("prefix", "suffix")

    def __init__(
        self,
        title_type: str,
        id: int | None = None,
    ):
        if title_type not in self.ALLOWED_TYPES:
            raise ValueError(f"title_type must be one of {self.ALLOWED_TYPES}, got '{title_type}'.")

        self.id = id
        self.title_type = title_type
