class DomainError(Exception):
    pass


class InvalidDataError(DomainError):
    pass


class ResourceNotFoundError(DomainError):
    pass
