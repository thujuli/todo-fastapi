from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    create_at = Column(DateTime(True), server_default=func.now())
    update_at = Column(DateTime(True), onupdate=func.now())

    projects = relationship("Project", back_populates="user")
