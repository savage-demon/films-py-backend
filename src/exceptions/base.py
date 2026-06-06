class AppError(Exception):
    pass

class EntityNotFoundError(AppError):
    pass

class BadRequestError(AppError):
    pass

class InternalServerError(AppError):
    pass
