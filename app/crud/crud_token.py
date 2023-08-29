from sqlalchemy.orm import Session
from app import models


def get_user_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
