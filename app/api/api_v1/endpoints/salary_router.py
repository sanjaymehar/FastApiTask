from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from app.controllers.salary_controller import create_salary, calculate_monthly_salary, get_salary_history
from typing import List, Annotated
from datetime import datetime

from app.models import User
from app.utils.auth import get_current_admin

salaries_router = APIRouter()
salaries_base_url = "/salaries"


class SalaryCreate(BaseModel):
    employee_id: int
    base_salary: float
    bonuses: float


class SalaryRecordSchema(BaseModel):
    base_salary: float
    bonuses: float
    created_at: datetime

    class Config:
        from_attributes = True


class SalaryHistoryResponseSchema(BaseModel):
    employee_id: int
    salary_history: List[SalaryRecordSchema]

    class Config:
        from_attributes = True


@salaries_router.post("")
def create_salary_endpoint(current_user: Annotated[User, Depends(get_current_admin)], salary: SalaryCreate, background_tasks: BackgroundTasks,
                           db: Session = Depends(get_db)):

    new_salary = create_salary(db, salary)
    background_tasks.add_task(calculate_monthly_salary, salary.employee_id, salary.base_salary, salary.bonuses, db)
    return {"status": "Salary data submitted", "data": new_salary}


@salaries_router.get("/salary-history/{employee_id}", response_model=dict)
def get_salary_history_api(
    employee_id: int,
    current_user: Annotated[User, Depends(get_current_admin)],
    db: Session = Depends(get_db)
):
    return get_salary_history(employee_id, db)
