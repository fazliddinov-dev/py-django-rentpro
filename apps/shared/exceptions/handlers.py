# apps/shared/exceptions/handlers.py

import re

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global exception handler for DRF.
    """
    # Let DRF handle standard exceptions first (ValidationError, NotFound, etc.)
    response = exception_handler(exc, context)
    if response is not None:
        return response

    # Handle database integrity errors
    if isinstance(exc, IntegrityError):
        error_message = str(exc)
        match = re.search(r"UNIQUE constraint failed: \w+\.(\w+)", error_message)
        if match:
            field_name = match.group(1)
            return Response(
                {field_name: [f"This {field_name} value already exists."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Database error occurred."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Handle serializer update assertion errors
    if isinstance(exc, AssertionError):
        error_message = str(exc)
        if "`update()` did not return an object instance" in error_message:
            return Response(
                {"detail": "Serializer update() must return the updated instance."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Generic AssertionError fallback
        return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)

    # Fallback for all other uncaught exceptions
    return Response(
        {"detail": "Internal server error."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
