import pytest

from app.api.api_v1.endpoints import salaries_base_url
from app.utils.constants import BASE_URL_V1
from test.base_test_case import BaseTestCase

TEST_URL = BASE_URL_V1 + salaries_base_url


class TestSalaryRoute(BaseTestCase):

    def test_read_employee_api(self, test_app):
        response = test_app.get(f"{TEST_URL}/salary-history/{self.employee_data.employee_exiting_user.get('id')}", headers=self.admin_access_token())
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    def test_read_employee_api_by_employee(self, test_app):
        response = test_app.get(f"{TEST_URL}/salary-history/{self.employee_data.employee_exiting_user.get('id')}", headers=self.employee_access_token())
        assert response.status_code == 403

    def test_read_non_exist_employee_api(self, test_app):
        response = test_app.get(f"{TEST_URL}/salary-history/6", headers=self.admin_access_token())
        assert response.status_code == 404

    def test_create_salary(self, test_app):
        response = test_app.post(f"{TEST_URL}/", json=self.salary_data.update_salary, headers=self.admin_access_token())
        response_data = response.json()
        assert response.status_code == 200
        assert isinstance(response_data, dict)
