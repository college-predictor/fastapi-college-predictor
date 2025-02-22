from fastapi import APIRouter

router = APIRouter()

@router.get("/maps_api", response_model=str)
def get_geocode_api_key():
    pass
