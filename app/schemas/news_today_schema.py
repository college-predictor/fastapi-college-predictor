from pydantic import BaseModel
from typing import List

class NewsSchema(BaseModel):
    title: str
    content: str
    url: str
    published_at: str
