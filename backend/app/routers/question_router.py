from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependencies import require_role
from app import models, schemas

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db),
                    teacher=Depends(require_role("teacher"))):

    worksheet = db.query(models.Worksheet).filter(models.Worksheet.id == question.worksheet_id).first()
    if not worksheet:
        raise HTTPException(status_code=404, detail="Worksheet not found")

    new_question = models.Question(
        question_text=question.question_text,
        worksheet_id=question.worksheet_id,
        created_by=teacher.id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


@router.get("/by-id/{question_id}", response_model=schemas.QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.get("/{worksheet_id}", response_model=list[schemas.QuestionResponse])
def list_questions(worksheet_id: int, db: Session = Depends(get_db)):
    return db.query(models.Question).filter(models.Question.worksheet_id == worksheet_id).all()