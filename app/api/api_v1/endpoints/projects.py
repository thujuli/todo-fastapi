from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas, models


router = APIRouter()


@router.post(
    "/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED
)
def create_project(
    data: schemas.ProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    project_dict = data.model_dump()
    project_dict.update({"user_id": current_user.id})
    new_project = models.Project(**project_dict)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get("/", response_model=list[schemas.ProjectOut])
def get_user_projects(
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    projects = (
        db.query(models.Project).filter(models.Project.user_id == current_user.id).all()
    )
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_user_project(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.user_id == current_user.id, models.Project.id == project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not Authorized to access this Project"
        )

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = db.query(models.Project).filter(
        models.Project.user_id == current_user.id, models.Project.id == project_id
    )

    project = query.first()
    if project is None:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not Authorized to delete this Project"
        )

    query.delete(synchronize_session=False)
    db.commit()


@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int,
    data: schemas.ProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = db.query(models.Project).filter(
        models.Project.user_id == current_user.id, models.Project.id == project_id
    )

    project = query.first()
    if project is None:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not Authorized to update this Project"
        )

    query.update(data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(project)

    return project
