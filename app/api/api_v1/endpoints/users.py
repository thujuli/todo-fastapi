from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app import schemas
from app.crud import crud_user

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    email_found = crud_user.get_user_email(db, user.email)
    if email_found:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "E-mail address already in use",
        )

    user_pswd = security.get_password_hash(user.password)
    new_user = crud_user.update_password(user, user_pswd)

    return crud_user.create_user(db, new_user)


@router.get("/me", response_model=schemas.UserOut)
def get_current_user(
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    return crud_user.get_user(db, current_user.id)
