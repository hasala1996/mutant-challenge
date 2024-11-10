from typing import List

from pydantic import BaseModel, field_validator


class DNARequest(BaseModel):
    dna: List[str]

    @field_validator("dna")
    @classmethod
    def check_dna_length(cls, value):
        if not value:
            raise ValueError("DNA list cannot be empty")

        length = len(value[0])
        if any(len(seq) != length for seq in value):
            raise ValueError("Each DNA string must have the same length")

        return value
