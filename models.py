import enum
from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    STAFF = "staff"
    VISITOR = "visitor"

class Gender(str, enum.Enum):
    MALE = "M"
    FEMALE = "F"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # 角色權限
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"), 
        default=UserRole.STUDENT, 
        nullable=False
    )
    
    # 學生詳細資料
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    student_id: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=True)
    class_name: Mapped[str] = mapped_column(String(50), nullable=True)  # 新增：班別 (Class Name)
    gender: Mapped[Gender] = mapped_column(Enum(Gender, name="gender_enum"), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    contact_number: Mapped[str] = mapped_column(String(20), nullable=True)

    # 帳號狀態與時間戳記
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
