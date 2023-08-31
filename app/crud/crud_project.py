from sqlalchemy.orm import Session, Query
from app import models, schemas


def get_project_by_title(db: Session, project_title: str, user_id: int):
    return (
        db.query(models.Project)
        .filter(
            models.Project.user_id == user_id,
            models.Project.title == project_title,
        )
        .first()
    )


def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    project_dict = project.model_dump()
    project_dict.update({"user_id": user_id})
    new_project = models.Project(**project_dict)

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


def get_user_projects(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()


def get_query_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id)


def delete_query(db: Session, query: Query):
    query.delete(synchronize_session=False)
    db.commit()


def update_query_project(db: Session, project: schemas.ProjectCreate, query: Query):
    project_updated = query.first()
    query.update(project.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(project_updated)

    return project_updated
