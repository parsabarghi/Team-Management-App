from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
import datetime

class PermissionType(str, Enum):
    """Permission types"""
    READ = "read"
    WRITE = "write" 
    DELETE = "delete"
    ADMIN = "admin"

class Resource(str, Enum):
    """Resource types"""
    USERS = "users"
    ROLES = "roles"
    PERMISSIONS = "permissions"
    SETTINGS = "settings"

class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str
    description: Optional[str] = None
    type: PermissionType
    resource: Resource

class PermissionCreate(PermissionBase):
    """Permission creation schema"""
    pass

class PermissionResponse(PermissionBase):
    """Permission response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

class RoleBase(BaseModel):
    """Base role schema"""
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    is_default: bool = False

class RoleCreate(RoleBase):
    """Role creation schema"""
    permissions: List[int] = []  # List of permission IDs

class RoleUpdate(BaseModel):
    """Role update schema"""
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = None
    is_default: Optional[bool] = None
    permissions: Optional[List[int]] = None

class RoleResponse(RoleBase):
    """Role response schema"""
    id: int
    permissions: List[PermissionResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True