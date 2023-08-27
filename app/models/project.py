from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    create_at = Column(DateTime(True), server_default=func.now())
    update_at = Column(DateTime(True), onupdate=func.now())

    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
