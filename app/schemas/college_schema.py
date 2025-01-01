from pydantic import BaseModel
from typing import Dict

class CollegeSchema(BaseModel):
    id: str
    courseName: str
    courseType: str
    collegeType: str
    collegeName: str
    instituteCode: int
    state: str
    gender: str
    quota: str
    category: str
    openingRank: int
    closingRank: int
    profileImage: str
    avgPkg: str
    nirfRanking: int
    placementRating: float
    collegeLifeRating: float
    campusRating: float
    aiSummary: str
    year: int
    contactInfo: Dict[str, str]