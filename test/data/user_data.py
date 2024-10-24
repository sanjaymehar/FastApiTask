from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = pwd_context.hash("hashed_password123")


class UserData:
    @property
    def admin_exiting_user(self):
        return {
            "id": 2,
            "username": "admin",
            "role": "admin",
            "hashed_password": f"{hashed_password}",
    }

    @property
    def employee_exiting_user(self):
        return {
            "id": 3,
            "username": "employee1",
            "role": "employee",
            "hashed_password": f"{hashed_password}",
    }

    @property
    def admin_login_data(self):
        return {
            "username": "admin",
            "password": "hashed_password123",
    }
    @property
    def admin_wrong_login_data(self):
        return {
            "username": "admin",
            "password": "hashed_password",
    }

    @property
    def create_user_data(self):
        return {
            "username": "employee2",
            "role": "employee",
            "password": "hashed_password123",
    }

    @property
    def create_already_exist_user_data(self):
        return {
            "username": "employee1",
            "role": "employee",
            "password": "hashed_password123",
    }
