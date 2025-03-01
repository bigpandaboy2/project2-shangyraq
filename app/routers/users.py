from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import models, schemas
from ..database import get_db
from ..security import (
    get_password_hash, verify_password, create_access_token, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth/users", tags=["Users"])

@router.post("/", status_code=200)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    hashed_pw = get_password_hash(user_data.password)
    new_user = models.User(
        username=user_data.username,
        password_hash=hashed_pw,
        phone=user_data.phone,
        name=user_data.name,
        city=user_data.city
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login", response_model=schemas.Token, status_code=200)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token}

@router.patch("/me", status_code=200)
def update_current_user(
    update_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if update_data.phone is not None:
        current_user.phone = update_data.phone
    if update_data.name is not None:
        current_user.name = update_data.name
    if update_data.city is not None:
        current_user.city = update_data.city

    db.commit()
    db.refresh(current_user)
    return {"message": "User data updated successfully"}

@router.get("/me", response_model=schemas.UserOut, status_code=200)
def get_current_user_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return current_user
