from adapters.api.dependencies import get_db
from adapters.database.repository.dna_repository import SQLAlchemyDNARepository
from core.mutant.services import MutantService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_dna_service(db: Session = Depends(get_db)) -> MutantService:
    """
    Dependency function that provides a `MutantService` instance.

    :param db: A database session to be injected, provided by the `get_db` dependency.
    :return: An instance of `MutantService` initialized with a `SQLAlchemyDNARepository`.
    """
    dna_repository = SQLAlchemyDNARepository(db)
    return MutantService(dna_repository)
