from test.data.employee_data import EmployeeData


class SalaryData(EmployeeData):
    @property
    def existing_salary(self):
        return {
            "id": 2,
            "employee_id": EmployeeData().existing_employee.get('employee_id'),
            "base_salary": 50000.00,
            "bonuses": 5000.00,
            "created_at": "2024-01-15 10:30:00"
        }

    @property
    def update_salary(self):
        return {
            "employee_id": EmployeeData().existing_employee.get('employee_id'),
            "base_salary": 60000.00,
            "bonuses": 1000.00,
        }
