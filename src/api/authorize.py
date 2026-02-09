import os

import allure
import requests

from src.api.base_api import BaseApi
from .constants import BASE_URL, AUTHORIZE_PATH
from dotenv import set_key, find_dotenv


class Authorize(BaseApi):
    url = BASE_URL + AUTHORIZE_PATH

    @allure.step('POST /authorize - Авторизация пользователя')
    def create_auth(self, name):
        body = {'name': name}
        with allure.step(f'Отправляем запрос с именем: {name}'):
            self.response = requests.post(self.url, json=body)
            if self.response.status_code == 200:
                self.response_json = self.response.json()
                self.token = self.response_json.get("token")
                self.save_token_to_env(self.token)
            else:
                self.response_json = None
                self.token = None
            return self.token

    @allure.step('GET /authorize/ - Проверка токена')
    def check_token(self, token):
        if not token:
            with allure.step('Токен не предоставлен'):
                return False
        with allure.step(f'Проверяем токен: {token[:10]}...'):
            try:
                self.response = requests.get(f'{self.url}/{token}')

                if self.response.status_code == 200:
                    with allure.step('Токен валиден'):
                        return True
                else:
                    with allure.step(f'Токен невалиден. Статус: {self.response.status_code}'):
                        return False
            except Exception as e:
                with allure.step(f'Ошибка при проверке токена: {e}'):
                    return False

    @allure.step('Получаем токен')
    def get_valid_token(self, name=None):
        if self.token is None:
            self.create_auth(name)
        else:
            self.check_token()
        return self.token

    @allure.step('')
    def check_token_key_in_response(self):
        assert "token" in self.response_json

    @allure.step('')
    def check_token_value_is_str(self):
        assert isinstance(self.token, str)

    @allure.step('')
    def check_token_value_is_not_empty(self):
        assert len(self.token) > 0

    @allure.step('')
    def save_token_to_env(self, token):
        env_path = find_dotenv()

        if env_path:
            set_key(env_path, 'TEST_TOKEN', token)
            with allure.step(f'Токен сохранен в .env: {token[:10]}...'):
                pass
