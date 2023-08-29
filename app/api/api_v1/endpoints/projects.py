from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_project
from app import schemas


router = APIRouter()


@router.post(
    "/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    project_found = crud_project.get_project_by_title(
        db, project.title, current_user.id
    )
    if project_found:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Can't create project with same title"
        )

    return crud_project.create_project(db, project, current_user.id)


@router.get("/", response_model=list[schemas.ProjectOut])
def get_user_projects(
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    return crud_project.get_user_projects(db, current_user.id)


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_user_project(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = crud_project.query_project(db, project_id)
    project = query.first()
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not authorized to access this project"
        )

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = crud_project.query_project(db, project_id)
    project = query.first()
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not authorized to delete this project"
        )

    query.delete(synchronize_session=False)
    db.commit()


@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = crud_project.query_project(db, project_id)
    project_found = query.first()
    if project_found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    if project_found.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not authorized to update this project"
        )

    project_by_title = crud_project.get_project_by_title(
        db, project.title, current_user.id
    )
    if project_by_title:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Project with title {project.title} exist, can't update",
        )

    return crud_project.update_query_project(db, project, query)
