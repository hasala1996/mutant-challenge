from typing import List

from adapters.database.repository.dna_repository import DNARepository


class MutantService:
    def __init__(self, dna_repository: DNARepository):
        """
        Initializes the MutantService with a DNA repository.

        :param dna_repository: An instance of DNARepository for accessing DNA records.
        """
        self.dna_repository = dna_repository

    def is_mutant(self, dna: List[str]) -> bool:
        """
        Determines if a given DNA sequence belongs to a mutant.

        This method checks for specific patterns within the DNA sequences to identify mutant characteristics
        based on horizontal, vertical, and diagonal alignments.

        :param dna: A list of strings, each representing a row in the DNA matrix.
        :return: True if the DNA sequence is identified as mutant, False otherwise.
        """

        def has_sequence(line):
            return any(
                line[i] == line[i + 1] == line[i + 2] == line[i + 3]
                for i in range(len(line) - 3)
            )

        size = len(dna)
        count = 0

        for i in range(size):
            if has_sequence(dna[i]):  # Horizontal
                count += 1
            if has_sequence([dna[j][i] for j in range(size)]):  # Vertical
                count += 1
            if count > 1:
                return True

        for i in range(size - 3):
            for j in range(size - 3):
                if (
                    dna[i][j]
                    == dna[i + 1][j + 1]
                    == dna[i + 2][j + 2]
                    == dna[i + 3][j + 3]
                ):
                    count += 1
                if (
                    dna[i][j + 3]
                    == dna[i + 1][j + 2]
                    == dna[i + 2][j + 1]
                    == dna[i + 3][j]
                ):
                    count += 1
                if count > 1:
                    return True

        return False

    def check_and_save_dna(self, dna: List[str]) -> bool:
        """
        Checks if the provided DNA sequence is mutant and saves it to the database if it's new.

        If the DNA sequence doesn't exist in the database, it will be saved along with its classification
        as mutant or human. If it exists, the method returns its current classification.

        :param dna: A list of strings, each representing a row in the DNA matrix.
        :return: True if the DNA sequence is mutant, False otherwise.
        """

        dna_sequence = "".join(dna)
        existing_dna = self.dna_repository.get_dna_by_sequence(dna_sequence)
        if existing_dna:
            return existing_dna.is_mutant

        is_mutant_flag = self.is_mutant(dna)
        self.dna_repository.create_dna_record(dna_sequence, is_mutant_flag)
        return is_mutant_flag

    def get_stats(self):
        """
        Retrieves statistics about the DNA records in the database.

        The statistics include the count of mutant and human DNA sequences,
        along with the ratio of mutants to total DNA sequences analyzed.

        :return: A dictionary containing counts of mutant and human DNA, and the mutant-to-total ratio.
        """
        count_mutant_dna = self.dna_repository.count_mutants()
        count_human_dna = self.dna_repository.count_humans()
        total = count_mutant_dna + count_human_dna
        ratio = count_mutant_dna / total if total > 0 else 0

        return {
            "count_mutant_dna": count_mutant_dna,
            "count_human_dna": count_human_dna,
            "ratio": ratio,
        }
