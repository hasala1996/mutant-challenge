"""
Custom exceptions
"""

from fastapi import status


class ValidationError(Exception):
    """
    Custom exception for validation errors.

    This exception is raised when there is a validation error in the application.
    It includes a status code (400 Bad Request) and a detailed error message"""

    def __init__(self, detail: str):
        """Init the validation error"""
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail


class IntegrityError(Exception):
    """
    Custom exception for integrity errors.

    This exception is raised when there is a data integrity issue, such as unique constraint violations.
    It includes a status code (400 Bad Request) and a detailed error message."""

    def __init__(self, detail: str):
        """Init the IntegrityError"""

        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail


class CustomAPIException(Exception):
    """
    Custom exception for general API errors.

    This exception is raised for various types of API errors, with customizable status codes and messages.
    It includes a status code and a detailed error message."""

    def __init__(self, detail: str, status_code: int):
        """Initialize the CustomAPIException"""
        self.status_code = status_code
        self.detail = detail
