from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependencies import require_role
from app import models, schemas

router = APIRouter(prefix="/workbooks", tags=["workbooks"])


@router.post("/", response_model=schemas.WorkbookResponse)
def create_workbook(workbook: schemas.WorkbookCreate, db: Session = Depends(get_db),
                    director=Depends(require_role("director"))):

    new_workbook = models.Workbook(
        title=workbook.title,
        created_by=director.id
    )
    db.add(new_workbook)
    db.commit()
    db.refresh(new_workbook)
    return new_workbook


@router.get("/", response_model=list[schemas.WorkbookResponse])
def list_workbooks(db: Session = Depends(get_db)):
    return db.query(models.Workbook).all()