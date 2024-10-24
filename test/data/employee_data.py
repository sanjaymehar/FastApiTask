from datetime import date

from test.data.user_data import UserData


class EmployeeData(UserData):
    @property
    def existing_employee(self):
        return {
            "id": 2,
            "employee_id": UserData().employee_exiting_user.get('id'),
            "name": "Kiran",
            "designation": "Software Engineer",
            "department": "Engineering",
            "joining_date": date(2023, 5, 1).isoformat(),
            "monthly_salary": 5000.0
        }

    @property
    def new_employee(self):
        return {
            "employee_id": 3,
            "name": "Rajesh",
            "designation": "Product Manager",
            "department": "Product",
            "joining_date": date(2023, 5, 1).isoformat(),
        }

    @property
    def update_employee(self):
        return {
            "name": "Jane Doe",  # Updated name
            "designation": "Senior Product Manager",  # Updated designation
            "department": "Product",
            "joining_date": date(2023, 5, 1).isoformat(),  # Same joining date
        }