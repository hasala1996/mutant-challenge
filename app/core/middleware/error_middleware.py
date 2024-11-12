"""
Error Middleware
"""

import logging

from core.exceptions.custom_exceptions import (
    CustomAPIException,
    IntegrityError,
    ValidationError,
)
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for centralized error handling in FastAPI.

    This middleware catches and handles custom exceptions such as `ValidationError`, `IntegrityError`,
    and `CustomAPIException`, as well as general exceptions. It returns appropriate JSON responses
    with error messages and status codes."""

    async def dispatch(self, request: Request, call_next):
        """
        Intercepts and processes the request, handling any exceptions.
        """
        try:
            response = await call_next(request)
            return response
        except ValidationError as exc:
            logging.error("ValidationError %s: ", exc)
            return JSONResponse(
                {"message": "Validation error", "code": "ValidationError"},
                status_code=exc.status_code,
            )
        except IntegrityError as exc:
            logging.error("IntegrityError: %s", exc)
            return JSONResponse(
                {"message": "Integrity error", "code": "INT001"},
                status_code=exc.status_code,
            )
        except CustomAPIException as exc:
            logging.error("CustomAPIException: %s", exc)
            return JSONResponse(
                {"message": "Conctact admin site", "code": str(exc.status_code)},
                status_code=exc.status_code,
            )
        except Exception as exc:
            logging.error("Unexpected error: %s", exc)
            return JSONResponse(
                {
                    "message": "An unexpected error occurred",
                    "details": "Contact admin site",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
