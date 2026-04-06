from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

from datetime import date
from typing import Optional

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: Optional[str]
    date: Optional[date]
    notes: Optional[str]

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: Optional[str]
    date: date
    notes: Optional[str]

    class Config:
        from_attributes = True