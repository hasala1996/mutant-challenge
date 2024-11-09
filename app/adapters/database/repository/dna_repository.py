from adapters.database.models.dna_model import DNA
from core.mutant.ports.repository import DNARepository
from sqlalchemy.orm import Session


class SQLAlchemyDNARepository(DNARepository):
    def __init__(self, db: Session):
        self.db = db

    def get_dna_by_sequence(self, sequence: str):
        return self.db.query(DNA).filter(DNA.sequence == sequence).first()

    def create_dna_record(self, sequence: str, is_mutant: bool):
        dna = DNA(sequence=sequence, is_mutant=is_mutant)
        self.db.add(dna)
        self.db.commit()
        return dna

    def count_mutants(self) -> int:
        return self.db.query(DNA).filter(DNA.is_mutant == True).count()

    def count_humans(self) -> int:
        return self.db.query(DNA).filter(DNA.is_mutant == False).count()
