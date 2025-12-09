from sqlalchemy import Table, ForeignKey, Column
from .base_class import Base

role_permission = Table(
    "role_permission", 
    Base.metadata, 
    Column("permission_id", ForeignKey("permission_id"), primary_key=True), 
    Column("role_id", ForeignKey("role_id"), primary_key=True)
)