from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Domain error raised by services; rendered as {"error": {"code", "message"}}."""

    def __init__(self, code: str, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


async def app_error_handler(_request: Request, error: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=error.status,
        content={"error": {"code": error.code, "message": error.message}},
    )
