from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from app.database import Base
from sqlalchemy.sql import func


class Salary(Base):
    __tablename__ = "salaries"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id', ondelete="CASCADE"), index=True)
    base_salary = Column(Float)
    bonuses = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
