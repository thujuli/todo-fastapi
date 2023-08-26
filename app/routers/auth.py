from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, db, models, security

router = APIRouter(prefix="", tags=["authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(db.get_db),
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if user is None or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect Email or Password",
            {"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
