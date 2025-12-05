from pydantic import BaseModel, Field
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from datetime import datetime

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    """Generic success response schema"""
    success: bool = True
    message: str
    data: Optional[T] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema"""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    error: str
    detail: Optional[Union[str, Dict[str, Any]]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ValidationErrorDetail(BaseModel):
    """Validation error detail schema"""
    loc: List[Union[str, int]]
    msg: str
    type: str

class ValidationErrorResponse(ErrorResponse):
    """Validation error response schema"""
    detail: List[ValidationErrorDetail]

class AuthErrorResponse(ErrorResponse):
    """Authentication error response schema"""
    code: str = "authentication_failed"
    detail: str