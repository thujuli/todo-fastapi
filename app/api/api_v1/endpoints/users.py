from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app import schemas, models

# from .. import schemas, db, models, security

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    # check email exist in db
    query = db.query(models.User).filter(models.User.email == user.email)
    if query.first():
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "E-mail address already in use",
        )

    # hashing user password
    user_pswd = security.get_password_hash(user.password)

    # update password and add to db
    user_dict = user.model_dump()
    user_dict.update({"password": user_pswd})
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me", response_model=schemas.UserOut)
def get_current_user(
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user
