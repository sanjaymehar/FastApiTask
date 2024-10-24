from typing import Optional, List, Annotated, Union
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import date
from app.database import get_db
from sqlalchemy.orm import Session
from app.controllers.employee_controller import (
    create_employee, update_employee,
    delete_employee, get_all_employee,
    get_employee_by_id
)
from app.models import User
from app.utils.auth import get_current_user, get_current_admin

employee_router = APIRouter()
employee_base_url = "/employee"


class EmployeeCreateSchema(BaseModel):
    employee_id: int
    name: str
    designation: str
    department: str
    joining_date: date


class EmployeeSchema(BaseModel):
    id: int
    employee_id: int
    name: str
    designation: str
    department: str
    joining_date: date
    monthly_salary: Optional[float] = None


class EmployeeUpdateSchema(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    joining_date: Optional[date] = None


@employee_router.get("", response_model=Optional[Union[List[EmployeeSchema], EmployeeSchema]])
def read_users_api(current_user: Annotated[User, Depends(get_current_user)],skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if current_user.role == 'admin':
        return get_all_employee(skip,limit,  db)
    elif current_user.role == 'employee':
        return get_employee_by_id(db, current_user.id)


@employee_router.post("", response_model=EmployeeSchema)
def create_employee_api(current_user: Annotated[User, Depends(get_current_admin)],
                        employee: EmployeeCreateSchema, db: Session = Depends(get_db)):
    return create_employee(employee, db)


@employee_router.put("/{employee_id}", response_model=EmployeeSchema)
def update_employee_api(current_user: Annotated[User, Depends(get_current_admin)],
                        employee_id: int, user: EmployeeUpdateSchema, db: Session = Depends(get_db)):
    return update_employee(employee_id, user, db)


@employee_router.delete("/{employee_id}")
def delete_user_api(current_user: Annotated[User, Depends(get_current_admin)],
                    employee_id: int, db: Session = Depends(get_db)):
    return delete_employee(employee_id, db)
