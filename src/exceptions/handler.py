from fastapi import Request
from fastapi.responses import JSONResponse
from src.exceptions.base import AppError, EntityNotFoundError

ERROR_MAP = {
    EntityNotFoundError: {
        "status_code": 404,
        "error_type": "Not Found",
    },
}

DEFAULT_ERROR = {
    "status_code": 500,
    "error_type": "Internal Server Error",
}


async def app_exception_handler(_request: Request, exc: AppError) -> JSONResponse:
    error = DEFAULT_ERROR

    for cls in type(exc).__mro__:
        if cls in ERROR_MAP:
            error = ERROR_MAP[cls]
            break

    return JSONResponse(
        status_code=error["status_code"],
        content={"error": error["error_type"], "message": exc.message},
    )


def register_exception_handlers(app):
    app.add_exception_handler(AppError, app_exception_handler)
