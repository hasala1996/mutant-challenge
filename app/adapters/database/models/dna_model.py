from sqlalchemy import Column, String, Boolean
from adapters.database.models.base_model import BaseModel


class DNA(BaseModel):
    __tablename__ = "dna_sequence"
    sequence = Column(String, unique=True, index=True)
    is_mutant = Column(Boolean)
