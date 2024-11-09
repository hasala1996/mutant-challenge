from typing import List

from adapters.database.repository.dna_repository import DNARepository


class MutantService:
    def __init__(self, dna_repository: DNARepository):
        self.dna_repository = dna_repository

    def is_mutant(self, dna: List[str]) -> bool:
        """Verifica si una secuencia de ADN es mutante"""

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
        """Verifica si la secuencia de ADN es mutante y la guarda en la base de datos si es nueva"""

        dna_sequence = "".join(dna)
        existing_dna = self.dna_repository.get_dna_by_sequence(dna_sequence)
        if existing_dna:
            return existing_dna.is_mutant

        is_mutant_flag = self.is_mutant(dna)
        self.dna_repository.create_dna_record(dna_sequence, is_mutant_flag)
        return is_mutant_flag

    def get_stats(self):
        count_mutant_dna = self.dna_repository.count_mutants()
        count_human_dna = self.dna_repository.count_humans()
        total = count_mutant_dna + count_human_dna
        ratio = count_mutant_dna / total if total > 0 else 0

        return {
            "count_mutant_dna": count_mutant_dna,
            "count_human_dna": count_human_dna,
            "ratio": ratio,
        }
