from adapters.api.endpoints import mutants
from fastapi import FastAPI

app = FastAPI()

# Registrar rutas
app.include_router(mutants.router, prefix="/mutant")


"""
Local file for debbug
"""

import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.api.endpoints import mutants
from app.core.middleware.error_middleware import ErrorHandlingMiddleware

logging.info("This is an info message")
load_dotenv(".env")

app = FastAPI()
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
    prefix="/api/v1/mutants",
    tags=["mutants"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
