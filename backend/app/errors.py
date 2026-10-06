from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Domain error raised by services; rendered as {"error": {"code", "message"}}."""

    def __init__(self, code: str, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


def _error_body(code: str, message: str) -> dict[str, dict[str, str]]:
    return {"error": {"code": code, "message": message}}


async def app_error_handler(_request: Request, error: AppError) -> JSONResponse:
    return JSONResponse(status_code=error.status, content=_error_body(error.code, error.message))


async def validation_error_handler(
    _request: Request, error: RequestValidationError
) -> JSONResponse:
    """Malformed requests use the same envelope as every other error, so the frontend parses
    one shape. Each problem reads like "body.daily_goal_xp: Value error, ..."."""
    problems = [
        f"{'.'.join(str(part) for part in problem['loc'])}: {problem['msg']}"
        for problem in error.errors()
    ]
    return JSONResponse(
        status_code=422, content=_error_body("VALIDATION_ERROR", "; ".join(problems))
    )
