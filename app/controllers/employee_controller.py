from app.models import Employee, User
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()


def get_all_employee(skip, limit, db):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees


def create_employee(employee, db: Session):
    # Check if employee_id already exists
    db_user = db.query(User).filter(User.id == employee.employee_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user's role is "employee"
    if db_user.role != "employee":
        raise HTTPException(status_code=403, detail="User does not have an employee role")

    # Check if employee_id already exists
    db_employee = get_employee_by_id(db, employee.employee_id)
    if db_employee:
        raise HTTPException(status_code=404, detail="Employee already registered")

    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(employee_id,  db: Session):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"detail": "Employee deleted successfully"}


def update_employee(employee_id, employee_update, db: Session):
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=400, detail="Employee ID not exists")

    for field, value in employee_update.dict(exclude_unset=True).items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee
