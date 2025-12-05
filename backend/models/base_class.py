from typing import Any
from sqlalchemy.orm import as_declarative
from sqlalchemy.ext.declarative import declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str 


    # to generate tablename from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
