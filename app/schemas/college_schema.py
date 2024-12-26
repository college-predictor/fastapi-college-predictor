from pydantic import BaseModel
from typing import List

class CollegeSchema(BaseModel):
    id: int
    courseName: str
    courseType: str
    collegeName: str
    seatType: str
    openingRank: int
    closingRank: int
    profileImage: str
    avgPkg: str
    nirfRanking: int
    placementRating: float
    collegeLifeRating: float
    campusRating: float
    aiSummary: str
    contactInfo: dict
