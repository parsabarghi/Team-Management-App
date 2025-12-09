from sqlalchemy import Column, Integer, String
from .base_class import Base


class Role(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False, unique=True)