from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_task
from app import schemas, models

router = APIRouter()


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    new_task: schemas.TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    project = crud_task.get_project(db, new_task.project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not authorized to use this project"
        )

    task_by_project = (
        db.query(models.Task)
        .filter(models.Task.project_id == new_task.project_id)
        .all()
    )
    for task in task_by_project:
        if task.title == new_task.title:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Can't create task with same title"
            )

    return crud_task.create_task(db, new_task)
