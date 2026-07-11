from app.domain.shared.value_objects.period import ValidityPeriod

class ModuleGroup:
    def __init__(
        self, 
        id: int, 
        name: str, 
        validity: ValidityPeriod,
    ):
        self.id = id
        self.name = name
        self.validity = validity