from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    is_done = Column(Boolean, server_default="false")
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    create_at = Column(DateTime(True), server_default=func.now())
    update_at = Column(DateTime(True), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
