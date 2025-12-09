from sqlalchemy import Column, Table, ForeignKey, PrimaryKeyConstraint, Integer
from .base_class import Base
from .role import Role


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("role_id", Integer, ForeignKey(Role.id)),
    PrimaryKeyConstraint("user_id", "role_id"),
)