from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import backref, relationship
from .base_class import Base
from .role_permission import role_permission


class Permission(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    roles = relationship(
        "Role",
        secondary=role_permission,
        backref=backref("permissions", lazy=True),
        lazy="subquery",
    )
    ### the roles have many-to-many relation, one role can have many permission, one permission can assigned to many roles.