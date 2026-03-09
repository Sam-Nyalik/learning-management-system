from pydantic import BaseModel
from typing import Optional

class GradeResponse(BaseModel):
    id: int
    answer_id: int
    teacher_id: int
    grade: int
    feedback: Optional[str]
    approved: bool

    class Config:
        from_attributes = True
