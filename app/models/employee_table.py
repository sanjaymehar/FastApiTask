from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    name = Column(String)
    designation = Column(String)
    department = Column(String)
    joining_date = Column(Date)
    monthly_salary = Column(Float, default=0.0)

    # Relationship with User and Salary
    user = relationship("User", back_populates="employees")
    salaries = relationship("Salary", backref="employee", cascade="all, delete-orphan", passive_deletes=True)
