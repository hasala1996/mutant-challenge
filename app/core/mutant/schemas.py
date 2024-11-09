from pydantic import BaseModel
from typing import List


class DNARequest(BaseModel):
    dna: List[str]
