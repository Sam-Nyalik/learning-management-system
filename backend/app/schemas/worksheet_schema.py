from pydantic import BaseModel

class WorksheetCreate(BaseModel):
    title: str
    workbook_id: int

class WorksheetResponse(BaseModel):
    id: int
    title: str
    workbook_id: int

    class Config:
        from_attributes = True
