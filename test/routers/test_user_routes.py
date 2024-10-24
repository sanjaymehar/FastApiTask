import pytest

from app.api.api_v1.endpoints import user_base_url
from test.base_test_case import BaseTestCase

TEST_URL = user_base_url



class TestUserRoute(BaseTestCase):

    def test_read_users_admin(self, test_app):
        response = test_app.get(f"{TEST_URL}/", headers= self.admin_access_token())
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, list)
        assert response_data == [{'id': self.user_data.admin_exiting_user.get('id'), 'username': self.user_data.admin_exiting_user.get('username'), 'role': self.user_data.admin_exiting_user.get('role')}, {'id': self.user_data.employee_exiting_user.get('id'), 'username': self.user_data.employee_exiting_user.get('username'), 'role': self.user_data.employee_exiting_user.get('role')}]

    def test_read_users_by_employee(self, test_app):
        response = test_app.get(f"{TEST_URL}/", headers=self.employee_access_token())
        assert response.status_code == 403

    def test_create_token_for_login(self, test_app):
        response = test_app.post(f"{TEST_URL}/login", json=self.user_data.admin_login_data)
        response_data = response.json()
        assert response_data == {'access_token': response_data.get("access_token"), 'token_type': 'bearer'}
        assert response.status_code == 200

    def test_create_token_for_login_with_incorrect_cred(self, test_app):
        response = test_app.post(f"{TEST_URL}/login", json=self.user_data.admin_wrong_login_data)
        assert response.status_code == 401

    def test_create_user(self, test_app):
        response = test_app.post(f"{TEST_URL}/", json=self.user_data.create_user_data)
        assert response.status_code == 200

    def test_already_exist_create_user(self, test_app):
        response = test_app.post(f"{TEST_URL}/", json=self.user_data.create_already_exist_user_data)
        assert response.json() == {'detail': 'username already registered'}
        assert response.status_code == 400

