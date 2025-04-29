from fastapi import APIRouter
from app.config.database import MongoDB
from app.models.college_model import CollegeModel
from app.services.college_service import CollegeService

router = APIRouter()

# Initialize database and service
db_client = MongoDB()
db_client.connect()
college_model = CollegeModel(db_client)
college_service = CollegeService(college_model)

@router.get("/colleges", response_model=dict)
def get_colleges(
    mains_gen_rank: int = None,
    mains_cat_rank: int = None,
    adv_gen_rank: int = None,
    adv_cat_rank: int = None,
    margin: float = 0.3,  # Default margin value set to 0.5
    category: str = "OPEN",  # Default category set to OPEN
    gender: str = "Gender-Neutral",  # Default gender set to Gender-Neutral
    state: str = None,  # Default state is None
    year: int = 2024
):
    """
    Fetches colleges based on provided rank criteria.
    API key validation is required.
    """
    if gender == "Female":
        gender = "Female-only (including Supernumerary)"
    else:
        gender = "Gender-Neutral"
        
    iit_colleges = college_service.fetch_iit_colleges(
        adv_gen_rank=adv_gen_rank,
        adv_cat_rank=adv_cat_rank,
        category=category,
        margin=margin,
        gender=gender,
        state=state,
        year=year
    )

    nit_colleges, iiit_colleges, gfti_colleges = college_service.fetch_mains_colleges(
        mains_gen_rank=mains_gen_rank,
        mains_cat_rank=mains_cat_rank,
        category=category,
        margin=margin,
        gender=gender,
        state=state,
        year=year
    )

    return {
        "iit_colleges": iit_colleges,
        "nit_colleges": nit_colleges,
        "iiit_colleges": iiit_colleges,
        "gfti_colleges": gfti_colleges,
    }