from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.config import Settings, get_settings
from app.controllers.user_controller import make_access_token, create_user, read_users
from app.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from enum import Enum
from app.models import User
from app.utils.auth import authenticate_user, get_current_admin

user_router = APIRouter()
user_base_url = "/user"


class UserRole(str, Enum):
    admin = "admin"
    employee = "employee"


class UserCreateSchem(BaseModel):
    username: str
    password: str
    role: UserRole


class UserSchema(BaseModel):
    id: int
    username: str
    role: UserRole

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str
    password: str


@user_router.post("", response_model=UserSchema)
def create_user_api(user: UserCreateSchem, db: Session = Depends(get_db)):
    return create_user(user, db)


@user_router.get("", response_model=List[UserSchema])
def read_users_api(current_user: Annotated[User, Depends(get_current_admin)],skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return read_users(skip,limit,  db)


@user_router.post("/login")
def login_for_access_token(
        settings: Annotated[Settings, Depends(get_settings)],
        user_login: UserLoginSchema,
        db: Session = Depends(get_db)
):

    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = make_access_token(user, settings)
    return {"access_token": access_token, "token_type": "bearer"}
