from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependencies import require_role
from app import models, schemas

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post("/", response_model=schemas.AnswerResponse)
def submit_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db),
                  student=Depends(require_role("student"))):

    question = db.query(models.Question).filter(models.Question.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    existing = db.query(models.Answer).filter(
        models.Answer.question_id == answer.question_id,
        models.Answer.student_id == student.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Answer already submitted")

    new_answer = models.Answer(
        question_id=answer.question_id,
        student_id=student.id,
        answer_text=answer.answer_text
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


@router.get("/my-answers", response_model=list[schemas.AnswerResponse])
def my_answers(student=Depends(require_role("student")), db: Session = Depends(get_db)):
    return db.query(models.Answer).filter(models.Answer.student_id == student.id).all()


@router.get("/all", response_model=list[schemas.AnswerResponse])
def all_answers(teacher=Depends(require_role("teacher")), db: Session = Depends(get_db)):
    return db.query(models.Answer).all()