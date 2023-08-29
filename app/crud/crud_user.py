from sqlalchemy.orm import Session
from app import models, schemas


def get_user_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def update_password(user: schemas.UserCreate, hashed_password: str):
    user_dict = user.model_dump()
    user_dict.update({"password": hashed_password})
    return models.User(**user_dict)


def create_user(db: Session, user: schemas.UserCreate):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
