from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import router as api_v1_router
from app.core.config import get_settings
from app.core.errors.exceptions import AppError
from app.core.errors.handlers import (
    app_error_handler,
    http_error_handler,
    unexpected_error_handler,
    validation_error_handler,
)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(
    StarletteHTTPException,
    http_error_handler,
)
app.add_exception_handler(
    RequestValidationError,
    validation_error_handler,
)
app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)

app.include_router(api_v1_router)


@app.get("/health", include_in_schema=False)
async def legacy_health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ragalink-api",
    }
