# core/dna/ports/repository.py
from abc import ABC, abstractmethod


class DNARepository(ABC):
    @abstractmethod
    def get_dna_by_sequence(self, sequence: str):
        pass

    @abstractmethod
    def create_dna_record(self, sequence: str, is_mutant: bool):
        pass

    @abstractmethod
    def count_mutants(self) -> int:
        pass

    @abstractmethod
    def count_humans(self) -> int:
        pass
