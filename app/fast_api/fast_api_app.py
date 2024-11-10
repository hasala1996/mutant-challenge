"""
FAST API
"""

import logging

import fastapi
from adapters.api.endpoints import mutants
from core.middleware.error_middleware import ErrorHandlingMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.info("This is an info message")


def create_app() -> fastapi.FastAPI:
    app = FastAPI()
    app.include_router(mutants.router, prefix="/mutant")

    """
    Main FastAPI application setup.

    This file configures the FastAPI application, including middleware for error handling,
    routes for users, authentication, onboarding, admin, and storage. It also loads environment variables
    and sets up dependency injection for services such as database connections.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    app.add_middleware(ErrorHandlingMiddleware)

    app.include_router(
        mutants.router,
        prefix="/api/v1",
        tags=["mutants"],
    )

    return app
