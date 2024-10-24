from app.controllers.employee_controller import get_employee_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import desc
from app.models import Salary


def calculate_monthly_salary(employee_id: int, base_salary: float, bonuses: float, db: Session):
    monthly_salary = base_salary + bonuses
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.monthly_salary = monthly_salary
    db.commit()


def create_salary(db: Session, salary):
    # Validate salary inputs
    if salary.base_salary < 0 or salary.bonuses < 0:
        raise HTTPException(status_code=400, detail="Salary and bonuses must be non-negative")

    # Check if the employee exists before adding salary
    employee = get_employee_by_id(db, salary.employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db_salary = Salary(**salary.dict())
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


def get_salary_history(employee_id: int, db: Session):

    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    salary_history = (
        db.query(Salary)
        .filter(Salary.employee_id == employee_id)
        .order_by(desc(Salary.created_at))
        .all()
    )

    formatted_history = [
        {
            "base_salary": record.base_salary,
            "bonuses": record.bonuses,
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Format date
        }
        for record in salary_history
    ]

    return {
        "employee_id": employee_id,
        "salary_history": formatted_history
    }
