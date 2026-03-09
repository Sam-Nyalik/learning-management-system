from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependencies import require_role
from app import models, schemas

router = APIRouter(prefix="/worksheets", tags=["worksheets"])

@router.post("/", response_model=schemas.WorksheetResponse)
def create_worksheet(worksheet: schemas.WorksheetCreate, db: Session = Depends(get_db),
                    director=Depends(require_role("director"))):
    
    workbook = db.query(models.Workbook).filter(models.Workbook.id == worksheet.workbook_id).first()
    if not workbook:
        raise HTTPException(status_code=404, detail="Workbook not found")

    new_worksheet = models.Worksheet(
        title=worksheet.title,
        workbook_id=worksheet.workbook_id
    )
    db.add(new_worksheet)
    db.commit()
    db.refresh(new_worksheet)
    return new_worksheet

@router.get("/{workbook_id}", response_model=list[schemas.WorksheetResponse])
def list_worksheets(workbook_id: int, db: Session = Depends(get_db)):
    return db.query(models.Worksheet).filter(models.Worksheet.workbook_id == workbook_id).all()
