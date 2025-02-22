from pydantic import BaseModel, Field, validator
from typing import List, Optional

class CounsellorRequest(BaseModel):
    message: str = Field(..., example="I need help choosing a college.")
    generate_research: bool = Field(
        False, description="Flag to indicate if research should be generated."
    )

    @validator("generate_research", pre=True, always=True)
    def set_generate_research_default(cls, v):
        return v or False

class CounsellorResponse(BaseModel):
    message_response: str
    questions: List[str]
    generate_research_generation: bool

class ResearchModel(BaseModel):
    research_id: str
    content: str
    generated_at: Optional[str] = None