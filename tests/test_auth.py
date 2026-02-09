import os

import allure
import pytest
from src.api.authorize import Authorize
from src.api.constants import INVALID_AUTH_TOKEN, TEST_USERNAME
from utils.body_data import get_invalid_authorization_name


@allure.feature('Авторизация')
@allure.story('Эндпоинт /authorize')
class TestAuthorization:

    @pytest.fixture(scope="class")
    def auth_endpoint(self):
        return Authorize()

    @allure.title('Проверка валидного токена')
    @pytest.mark.positive
    @pytest.mark.critical
    def test_check_valid_token(self, auth_token, auth_endpoint):
        is_valid = auth_endpoint.check_token(auth_token)

        assert is_valid == True, "Валидный токен должен проходить проверку"

    @allure.title('Авторизация с валидными данными')
    @pytest.mark.positive
    @pytest.mark.critical
    def test_authorize_valid_user(self, auth_endpoint):
        token = auth_endpoint.create_auth(TEST_USERNAME)
        auth_endpoint.assert_status_code(200)
        auth_endpoint.check_token_key_in_response()
        auth_endpoint.check_token_value_is_str()
        auth_endpoint.check_token_value_is_not_empty()

    @allure.title('Проверка невалидного токена')
    @pytest.mark.negative
    @pytest.mark.critical
    def test_check_invalid_token(self, auth_endpoint):
        is_valid = auth_endpoint.check_token(INVALID_AUTH_TOKEN)

        assert is_valid == False, "Невалидный токен должен не проходить проверку"

    @allure.title('Авторизация с невалидным именем: {invalid_data}')
    @pytest.mark.parametrize('invalid_data', get_invalid_authorization_name())
    @pytest.mark.negative
    @pytest.mark.medium
    def test_authorize_invalid_name(self, auth_endpoint, meme_endpoint, invalid_data):
        name_value = invalid_data.get('name') if isinstance(invalid_data, dict) else invalid_data
        authorize_endpoint_invalid = Authorize()
        authorize_endpoint_invalid.create_auth(name_value)
        authorize_endpoint_invalid.assert_status_code(400)
