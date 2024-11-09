from core.mutant.schemas import DNARequest
from core.mutant.services import MutantService
from dependencies.dna_service import get_dna_service
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/mutant/")
async def detect_mutant(
    dna_request: DNARequest, dna_service: MutantService = Depends(get_dna_service)
):
    is_mutant = dna_service.check_and_save_dna(dna_request.dna)
    if is_mutant:
        return {"message": "Mutant detected"}
    raise HTTPException(status_code=403, detail="Not a mutant")


@router.get("/stats/")
async def get_stats(dna_service: MutantService = Depends(get_dna_service)):
    return dna_service.get_stats()
