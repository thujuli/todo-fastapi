from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, db, models, security

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    # check email exist in db
    query = db.query(models.User).filter(models.User.email == user.email)
    if query.first():
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "E-mail address already in use.",
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


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
