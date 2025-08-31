from pydantic import BaseModel
from typing import Any

class ProblemCreate(BaseModel):
    title: str
    description: str
    test_cases: Any # Will be a JSON object

class Problem(ProblemCreate):
    id: int

    class Config:
        from_attributes = True
