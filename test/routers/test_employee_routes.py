import pytest

from app.api.api_v1.endpoints import employee_base_url
from app.utils.constants import BASE_URL_V1
from test.base_test_case import BaseTestCase

TEST_URL = BASE_URL_V1 + employee_base_url


class TestEmployeeRoute(BaseTestCase):

    def test_read_employee_api(self, test_app):
        response = test_app.get(f"{TEST_URL}/", headers=self.admin_access_token())
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, list)

    def test_read_employee_api_by_employee(self, test_app):
        response = test_app.get(f"{TEST_URL}/", headers= self.employee_access_token())
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    def test_patch_employee_api(self, test_app):

        response = test_app.put(f"{TEST_URL}/{self.employee_data.employee_exiting_user.get('id')}", headers=self.admin_access_token(),
                                  json=self.employee_data.update_employee)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    def test_patch_employee_api_by_employee(self, test_app):

        response = test_app.put(f"{TEST_URL}/{self.employee_data.employee_exiting_user.get('employee_id')}", headers=self.employee_access_token(),
                                  json=self.employee_data.update_employee)
        assert response.status_code == 403

    def test_delete_employee_api_by_employee(self, test_app):

        response = test_app.put(f"{TEST_URL}/{self.employee_data.employee_exiting_user.get('employee_id')}",
                                headers=self.employee_access_token(),
                                  )
        assert response.status_code == 403

    def test_delete_employee_api(self, test_app):

        response = test_app.delete(f"{TEST_URL}/{self.employee_data.existing_employee.get('employee_id')}",
                                   headers=self.admin_access_token(),
                                  )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    def test_create_employee_api_by_employee(self, test_app):
        response = test_app.post(f"{TEST_URL}/", json=self.employee_data.existing_employee,
                                 headers=self.employee_access_token())
        assert response.status_code == 403

    def test_create_existing_employee(self, test_app):
        response = test_app.post(f"{TEST_URL}/", json=self.employee_data.existing_employee, headers=self.admin_access_token())
        assert response.json() == {'detail': 'Employee already registered'}
        assert response.status_code == 404
