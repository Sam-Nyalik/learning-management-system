from pydantic import BaseModel

class WorkbookCreate(BaseModel):
    title: str

class WorkbookResponse(BaseModel):
    id: int
    title: str
    created_by: int

    class Config:
        from_attributes = True