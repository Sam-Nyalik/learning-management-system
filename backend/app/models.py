from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Index
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    email = Column(String, unique = True, index = True)
    password = Column(String)
    role = Column(String, index = True)

class Workbook(Base):
    __tablename__ = "workbooks"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"), index = True)

class Worksheet(Base):
    __tablename__ = "worksheets"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    workbook_id = Column(Integer, ForeignKey("workbooks.id"), index = True)

class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        Index("idx_question_creator", "id", "created_by"),
    )

    id = Column(Integer, primary_key = True, index = True)
    question_text = Column(Text)
    worksheet_id = Column(Integer, ForeignKey("worksheets.id"), index = True)
    created_by = Column(Integer, ForeignKey("users.id"), index = True)

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key = True, index = True)
    question_id = Column(Integer, ForeignKey("questions.id"), index = True)
    student_id = Column(Integer, ForeignKey("users.id"), index = True)
    answer_text = Column(Text)

class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = (
        Index("idx_teacher_answer", "teacher_id", "answer_id"),
    )

    id = Column(Integer, primary_key = True, index = True)
    answer_id = Column(Integer, ForeignKey("answers.id"), index = True)
    teacher_id = Column(Integer, ForeignKey("users.id"), index = True)
    grade = Column(Integer)
    feedback = Column(Text)
    approved = Column(Boolean, default = False, index = True)