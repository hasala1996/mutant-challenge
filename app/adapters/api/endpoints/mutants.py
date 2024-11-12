from core.mutant.schemas import DNARequest
from core.mutant.services import MutantService
from dependencies.dna_service import get_dna_service
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/mutant/")
async def detect_mutant(
    dna_request: DNARequest, dna_service: MutantService = Depends(get_dna_service)
):
    """
    Endpoint to determine if a DNA sequence belongs to a mutant and save the result.

    :param dna_request: The request body containing the DNA sequence.
    :param dna_service: Dependency injection of the MutantService for handling DNA analysis.
    :return: A message indicating whether a mutant DNA was detected.
    :raises HTTPException: 403 error if the DNA does not belong to a mutant.
    """
    is_mutant = dna_service.check_and_save_dna(dna_request.dna)
    if is_mutant:
        return {"message": "Mutant detected"}
    raise HTTPException(status_code=403, detail="Not a mutant")


@router.get("/stats/")
async def get_stats(dna_service: MutantService = Depends(get_dna_service)):
    """
    Endpoint to retrieve statistics about human and mutant DNA sequences.

    :param dna_service: Dependency injection of the MutantService for retrieving statistics.
    :return: A dictionary containing counts and ratio of mutant versus human DNA sequences.
    """
    return dna_service.get_stats()
