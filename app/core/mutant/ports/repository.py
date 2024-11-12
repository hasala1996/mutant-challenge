from abc import ABC, abstractmethod


class DNARepository(ABC):
    @abstractmethod
    def get_dna_by_sequence(self, sequence: str):
        """
        Retrieves a DNA record from the database based on the provided DNA sequence.

        :param sequence: The DNA sequence string used to search for an existing record.
        :return: An object representing the DNA record if found, otherwise None.
        """

    @abstractmethod
    def create_dna_record(self, sequence: str, is_mutant: bool):
        """
        Creates and stores a new DNA record in the database with its classification.

        :param sequence: The DNA sequence string to be stored.
        :param is_mutant: A boolean flag indicating whether the DNA sequence is mutant or not.
        """

    @abstractmethod
    def count_mutants(self) -> int:
        """
        Counts the number of mutant DNA records in the database.

        :return: The total number of mutant DNA sequences recorded.
        """

    @abstractmethod
    def count_humans(self) -> int:
        """
        Counts the number of human (non-mutant) DNA records in the database.

        :return: The total number of human DNA sequences recorded.
        """
