from sqlalchemy.orm import Session
from app import models
from . import auth_service

def create_user(db: Session, name: str, email: str, password: str, role: str):
    hashed_password = auth_service.hash_password(password)
    user = models.User(name=name, email=email, password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user