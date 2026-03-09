from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependencies import require_role
from app import models

router = APIRouter(prefix="/grades", tags=["grades"])


@router.post("/{answer_id}")
def grade_answer(answer_id: int, grade_value: int, feedback: str = "",
                 db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):

    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    grade = models.Grade(
        answer_id=answer_id,
        teacher_id=teacher.id,
        grade=grade_value,
        feedback=feedback,
        approved=False
    )
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return {"message": "Answer graded", "grade_id": grade.id}


@router.patch("/{grade_id}/approve")
def approve_grade(grade_id: int, db: Session = Depends(get_db),
                  director=Depends(require_role("director"))):

    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    grade.approved = True
    db.commit()
    return {"message": "Grade approved"}


@router.patch("/{grade_id}/reject")
def reject_grade(grade_id: int, db: Session = Depends(get_db),
                 director=Depends(require_role("director"))):

    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    grade.approved = False
    db.commit()
    return {"message": "Grade rejected"}


@router.get("/all", response_model=list)
def list_grades(db: Session = Depends(get_db)):
    return db.query(models.Grade).all()


@router.get("/report")
def grades_report(db: Session = Depends(get_db), director=Depends(require_role("director"))):
    """Returns all grades organised by workbook > worksheet > question for the director."""
    results = (
        db.query(
            models.Workbook.id.label("workbook_id"),
            models.Workbook.title.label("workbook_title"),
            models.Worksheet.id.label("worksheet_id"),
            models.Worksheet.title.label("worksheet_title"),
            models.Question.id.label("question_id"),
            models.Question.question_text,
            models.User.name.label("student_name"),
            models.Answer.answer_text,
            models.Grade.id.label("grade_id"),
            models.Grade.grade,
            models.Grade.feedback,
            models.Grade.approved,
        )
        .join(models.Worksheet, models.Worksheet.workbook_id == models.Workbook.id)
        .join(models.Question, models.Question.worksheet_id == models.Worksheet.id)
        .join(models.Answer, models.Answer.question_id == models.Question.id)
        .join(models.User, models.User.id == models.Answer.student_id)
        .join(models.Grade, models.Grade.answer_id == models.Answer.id)
        .all()
    )

    report = {}
    for row in results:
        wb_key = f"{row.workbook_id}:{row.workbook_title}"
        ws_key = f"{row.worksheet_id}:{row.worksheet_title}"
        if wb_key not in report:
            report[wb_key] = {"workbook_id": row.workbook_id, "workbook_title": row.workbook_title, "worksheets": {}}
        if ws_key not in report[wb_key]["worksheets"]:
            report[wb_key]["worksheets"][ws_key] = {"worksheet_id": row.worksheet_id, "worksheet_title": row.worksheet_title, "grades": []}
        report[wb_key]["worksheets"][ws_key]["grades"].append({
            "grade_id": row.grade_id,
            "question": row.question_text,
            "student": row.student_name,
            "answer": row.answer_text,
            "grade": row.grade,
            "feedback": row.feedback,
            "approved": row.approved,
        })

    output = []
    for wb in report.values():
        wb["worksheets"] = list(wb["worksheets"].values())
        output.append(wb)
    return output