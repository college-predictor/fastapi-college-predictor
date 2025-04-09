from fastapi import APIRouter
from app.services.rank_converter import convert_ranks

router = APIRouter()

@router.get("/convert-rank")
def convert_general_rank(gen_rank: int):
    """
    Convert a general rank to category-specific ranks (OBC, SC, ST, EWS).
    
    Args:
        gen_rank: The general rank to convert
        
    Returns:
        Dict containing converted ranks for each category
    """
    return convert_ranks(gen_rank)