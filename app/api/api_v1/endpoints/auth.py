from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas
from app.crud import crud_token
from app.api.deps import get_db
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = crud_token.get_user_email(db, form_data.username)
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect Email or Password",
            {"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
