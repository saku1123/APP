import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db, engine, Base
import models
import schemas
import auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="VTC-SAS API Service", version="1.0.0", lifespan=lifespan)

# ==========================================
# 1. Student Module (學生模組)
# ==========================================
@app.post("/api/v1/students/register", response_model=schemas.StudentProfileResponse, status_code=201, tags=["Student"])
async def register_student(data: schemas.StudentRegister, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(models.User).where(
            (models.User.username == data.username) | 
            (models.User.email == data.email) |
            (models.User.student_id == data.student_id)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username, Email or Student ID already exists")

    user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=auth.hash_password(data.password),
        role=models.UserRole.STUDENT,
        full_name=data.full_name,
        student_id=data.student_id,
        class_name=data.class_name,
        gender=data.gender,
        age=data.age,
        contact_number=data.contact_number
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.post("/api/v1/students/login", response_model=schemas.Token, tags=["Student"])
async def login_student(credentials: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.username == credentials.username, models.User.role == models.UserRole.STUDENT))
    user = result.scalar_one_or_none()

    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid student credentials")

    token = auth.create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/v1/students/me", response_model=schemas.StudentProfileResponse, tags=["Student"])
async def get_student_me(current_user: models.User = Depends(auth.get_current_student)):
    return current_user


# ==========================================
# 2. Staff Module (教職員模組)
# ==========================================
@app.post("/api/v1/staff/register", response_model=schemas.StaffProfileResponse, status_code=201, tags=["Staff"])
async def register_staff(data: schemas.StaffRegister, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(models.User).where(
            (models.User.username == data.username) | (models.User.email == data.email)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or Email already exists")

    user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=auth.hash_password(data.password),
        role=models.UserRole.STAFF,
        full_name=data.full_name,
        contact_number=data.contact_number
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.post("/api/v1/staff/login", response_model=schemas.Token, tags=["Staff"])
async def login_staff(credentials: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.username == credentials.username, models.User.role == models.UserRole.STAFF))
    user = result.scalar_one_or_none()

    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid staff credentials")

    token = auth.create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}


# ==========================================
# 3. Visitor Module (訪客模組)
# ==========================================
@app.post("/api/v1/visitors/register", response_model=schemas.VisitorProfileResponse, status_code=201, tags=["Visitor"])
async def register_visitor(data: schemas.VisitorRegister, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(models.User).where(
            (models.User.username == data.username) | (models.User.email == data.email)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or Email already exists")

    user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=auth.hash_password(data.password),
        role=models.UserRole.VISITOR,
        full_name=data.full_name,
        contact_number=data.contact_number
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.post("/api/v1/visitors/login", response_model=schemas.Token, tags=["Visitor"])
async def login_visitor(credentials: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.username == credentials.username, models.User.role == models.UserRole.VISITOR))
    user = result.scalar_one_or_none()

    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid visitor credentials")

    token = auth.create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}
