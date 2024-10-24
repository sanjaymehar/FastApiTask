from app.config import Settings
from app.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.utils.auth import get_password_hash, create_access_token
from datetime import timedelta


def create_user(user,  db: Session):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_users(skip, limit, db):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


def make_access_token(user: User, settings: Settings):
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires,settings=settings
    )
    return access_token



