# adapters/api/dependencies.py
from adapters.api.dependencies import get_db
from adapters.database.repository.dna_repository import SQLAlchemyDNARepository
from core.mutant.services import MutantService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_dna_service(db: Session = Depends(get_db)) -> MutantService:
    dna_repository = SQLAlchemyDNARepository(db)
    return MutantService(dna_repository)
