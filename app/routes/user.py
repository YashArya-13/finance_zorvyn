from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app import models, schemas
from app.database import SessionLocal
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from app.utils.role_checker import require_roles

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


# 📦 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 LOGIN API
@router.post("/login")
def login(user: schemas.LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role
        }
    }


# 👤 CREATE USER (Admin only)
@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
   # current_user = Depends(require_roles(["admin"]))
):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# 📄 GET ALL USERS (Any logged-in user)
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(models.User).all()


# ✏️ UPDATE USER (Admin only)
@router.put("/{user_id}")
def update_user(
    user_id: int,
    updated: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated.name
    user.email = updated.email
    user.password = hash_password(updated.password)
    user.role = updated.role

    db.commit()

    return {"message": "User updated successfully"}


# ❌ DELETE USER (Admin only)
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


# 🔄 ACTIVATE / DEACTIVATE USER (Admin only)
@router.patch("/{user_id}/status")
def change_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = is_active
    db.commit()

    return {
        "message": f"User {'activated' if is_active else 'deactivated'} successfully"
    }