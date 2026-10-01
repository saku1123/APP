from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import UserRole, Gender

# 通用登入 Request
class UserLogin(BaseModel):
    username: str
    password: str

# Token Response
class Token(BaseModel):
    access_token: str
    token_type: str

# 1. Student 相關 Schema
class StudentRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    student_id: str
    class_name: str
    gender: Gender
    age: int
    contact_number: str

class StudentProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    full_name: str
    student_id: str
    class_name: str
    gender: Gender
    age: int
    contact_number: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# 2. Staff 相關 Schema
class StaffRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    contact_number: str

class StaffProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    full_name: str
    contact_number: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# 3. Visitor 相關 Schema
class VisitorRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    contact_number: str

class VisitorProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    full_name: str
    contact_number: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
