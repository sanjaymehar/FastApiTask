import pytest
from fastapi.testclient import TestClient
from app.models import (Employee, Salary, User)
from app.config import get_settings
from app.controllers.user_controller import make_access_token
from app.database import SessionLocal, Base, engine
from test.data import (UserData, EmployeeData, SalaryData)
from contextlib import contextmanager
from sqlalchemy.exc import DBAPIError, IntegrityError
from fastapi import HTTPException, status



@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except DBAPIError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=exc.orig.args[0])
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=exc.orig.args[0])
    finally:
        db.close()


@pytest.mark.usefixtures("app")
class BaseTestCase:
    @pytest.fixture
    def test_app(self, app):

        Base.metadata.drop_all(bind=engine)
        test_client = TestClient(app)
        self.setup_test_data()
        yield test_client
        Base.metadata.drop_all(bind=engine)


    def setup_test_data(self):
        Base.metadata.create_all(bind=engine)
        self.user_data = UserData()
        self.user1_model = User(**self.user_data.admin_exiting_user)
        self.commit_data_model(self.user1_model)
        self.user2_model = User(**self.user_data.employee_exiting_user)
        self.commit_data_model(self.user2_model)

        self.employee_data = EmployeeData()
        self.employee_1_model = Employee(**self.employee_data.existing_employee)
        self.commit_data_model(self.employee_1_model)

        self.salary_data = SalaryData()
        self.salary_model = Salary(**self.salary_data.existing_salary)
        self.commit_data_model(self.salary_model)


    def commit_data_model(self, model):
        with get_db_session() as db_session:
            db_session.add(model)
            db_session.commit()
            db_session.refresh(model)

    def settings(self):
        return get_settings()

    def admin_access_token(self):
        token = make_access_token(self.user1_model, self.settings())
        self.headers = {"Authorization": f"Bearer {token}"}
        return self.headers

    def employee_access_token(self):
        token = make_access_token(self.user2_model, self.settings())
        self.headers = {"Authorization": f"Bearer {token}"}
        return self.headers

