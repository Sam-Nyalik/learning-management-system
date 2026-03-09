from pydantic import BaseModel

class QuestionCreate(BaseModel):
    question_text: str
    worksheet_id: int

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    worksheet_id: int
    created_by: int

    class Config:
        from_attributes = True