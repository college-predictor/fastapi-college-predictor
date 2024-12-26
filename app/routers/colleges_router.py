# from fastapi import APIRouter, Depends
# from app.schemas.college_schema import CollegeSchema
# from app.config.database import MongoDB
# from app.models.college_model import CollegeModel
# from app.services.college_service import CollegeService

# router = APIRouter()

# db_client = MongoDB()
# db_client.connect('college-predictor-dev')
# college_model = CollegeModel(db_client)
# college_service = CollegeService(college_model)

# @router.get("/colleges", response_model=list[CollegeSchema])
# def get_colleges(mains_gen_rank: int = None, mains_cat_rank: int = None, adv_gen_rank: int = None, adv_cat_rank: int = None):
#     return college_service.fetch_colleges(mains_gen_rank, mains_cat_rank, adv_gen_rank, adv_cat_rank)


from fastapi import APIRouter, Depends
from app.schemas.college_schema import CollegeSchema
from app.config.database import MongoDB
from app.models.college_model import CollegeModel
from app.services.college_service import CollegeService
from app.utils.security import validate_api_key

router = APIRouter()

# Initialize database and service
db_client = MongoDB()
db_client.connect('college-predictor-dev')
college_model = CollegeModel(db_client)
college_service = CollegeService(college_model)

@router.get("/colleges", response_model=list[CollegeSchema], dependencies=[Depends(validate_api_key)])
def get_colleges(
    mains_gen_rank: int = None,
    mains_cat_rank: int = None,
    adv_gen_rank: int = None,
    adv_cat_rank: int = None,
    margin: float = None,
    category: str = None,
    gender: str = None,
    state: str = None
):
    """
    Fetches colleges based on provided rank criteria.
    API key validation is required.
    """
    iit_colleges = college_service.fetch_iit_colleges(
        adv_gen_rank=adv_gen_rank,
        adv_cat_rank=adv_cat_rank,
    )
    nit_colleges = college_service.fetch_nit_colleges(
        mains_gen_rank=mains_gen_rank,
        mains_cat_rank=mains_cat_rank,
    )
    iiit_colleges = college_service.fetch_iiit_colleges(
        mains_gen_rank=mains_gen_rank,
        mains_cat_rank=mains_cat_rank,
    )
    gfti_colleges = college_service.fetch_gfti_colleges(
        mains_gen_rank=mains_gen_rank,
        mains_cat_rank=mains_cat_rank,
    )
    return {
        "iit_colleges": iit_colleges,
        "nit_colleges": nit_colleges,
        "iiit_colleges": iiit_colleges,
        "gfti_colleges": gfti_colleges,
    }