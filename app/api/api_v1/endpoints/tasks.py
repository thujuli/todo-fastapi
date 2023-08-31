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

    task_by_project = crud_task.get_tasks_by_project(db, new_task.project_id)
    for task in task_by_project:
        if task.title == new_task.title:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Can't create task with same title"
            )

    return crud_task.create_task(db, new_task)


@router.get("/", response_model=list[schemas.TaskOut])
def get_taks(
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    all_taks_current_user = crud_task.get_tasks_by_current_user(db, current_user.id)
    return all_taks_current_user


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = crud_task.query_get_task(db, task_id)
    task = query.first()
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    all_taks_current_user = crud_task.get_tasks_by_current_user(db, current_user.id)
    crud_task.err_if_task_id_not_in_tasks(
        all_taks_current_user,
        task_id,
        "User is not authorized to access this task",
    )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = crud_task.query_get_task(db, task_id)
    task = query.first()
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    all_taks_current_user = crud_task.get_tasks_by_current_user(
        db,
        current_user.id,
    )
    crud_task.err_if_task_id_not_in_tasks(
        all_taks_current_user,
        task_id,
        "User is not authorized to delete this task",
    )
    crud_task.delete_query(db, query)


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    new_task: schemas.TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.UserOut = Depends(deps.get_current_user),
):
    query = crud_task.query_get_task(db, task_id)
    task = query.first()
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    all_taks_current_user = crud_task.get_tasks_by_current_user(db, current_user.id)
    crud_task.err_if_task_id_not_in_tasks(
        all_taks_current_user,
        task_id,
        "User is not authorized to update this task",
    )

    project = crud_task.get_project(db, new_task.project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not authorized to use this project"
        )

    task_by_project = crud_task.get_tasks_by_project(db, new_task.project_id)
    for task in task_by_project:
        if task.title == new_task.title:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Can't create task with same title"
            )

    return crud_task.update_query_task(db, new_task, query)
