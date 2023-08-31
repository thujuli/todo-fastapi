from sqlalchemy.orm import Session, Query
from fastapi import HTTPException, status
from app import models, schemas


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_tasks_by_project(db: Session, project_id: int):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


def create_task(db: Session, task: schemas.TaskCreate):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks_by_current_user(db: Session, current_user_id: int) -> list[models.Task]:
    get_all_taks = (
        db.query(models.Project.user_id, models.Task)
        .join(models.Project)
        .filter(models.Task.project_id == models.Project.id)
        .all()
    )

    tasks = []
    for user_id, task in get_all_taks:
        if user_id == current_user_id:
            tasks.append(task)

    return tasks


def err_if_task_id_not_in_tasks(
    tasks: list[models.Task], task_id: int, detail_err: str
):
    """Pseudocode for solved this problem
    1. append all task_id to list
    2. if task_id not in list, raise error"""
    task_ids = []
    for task in tasks:
        task_ids.append(task.id)

    if task_id not in task_ids:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail_err,
        )


def query_get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id)


def delete_query(db: Session, query: Query):
    query.delete(synchronize_session=False)
    db.commit()


def update_query_task(db: Session, task: schemas.TaskCreate, query: Query):
    project_updated = query.first()
    query.update(task.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(project_updated)

    return project_updated
