from dotenv import load_dotenv

from utils.body_data import generate_meme_data

load_dotenv()

import os
import allure
import pytest

from src.api.authorize import Authorize
from src.api.base_api import BaseApi
from src.api.meme_endpoint import MemeEndpoint
from src.api.constants import TEST_USERNAME, TEST_TOKEN


@pytest.fixture(scope="session")
def auth_token():
    auth = Authorize()
    cached_token = os.environ.get('TEST_TOKEN') or TEST_TOKEN
    if cached_token:
        with allure.step(f'Проверяем кэшированный токен: {cached_token[:10]}...'):
            if auth.check_token(cached_token):
                with allure.step('Кэшированный токен валиден — используем его'):
                    return cached_token
            else:
                with allure.step('Кэшированный токен невалиден — создаем новый'):
                    pass
    with allure.step(f'Создаем новый токен для пользователя: {TEST_USERNAME}'):
        token = auth.create_auth(TEST_USERNAME)
        assert token is not None, "Не удалось создать токен"
        return token


@pytest.fixture(scope='session')
def base_api():
    return BaseApi()


@pytest.fixture(scope='function')
def meme_endpoint_without_token():
    endpoint = MemeEndpoint()
    return endpoint


@pytest.fixture(scope='function')
def meme_endpoint(auth_token):
    endpoint = MemeEndpoint()
    endpoint.set_token(auth_token)
    return endpoint


@pytest.fixture(scope='function')
def meme_id(meme_endpoint):
    data = generate_meme_data()
    meme_endpoint.create_meme(data)
    meme_id = meme_endpoint.meme_id
    with allure.step(f'Создан мем с ID: {meme_id}'):
        pass

    yield meme_id

    with allure.step(f'Очистка: удаляем мем с ID {meme_id}'):
        try:
            meme_endpoint.delete_meme(meme_id)
        except Exception as e:
            allure.attach(f'Ошибка при удалении: {e}', name='Cleanup error')

@pytest.fixture(scope='function')
def delete_meme(meme_endpoint):
    delete_list = []

    def add_meme_id(meme_id):
        if meme_id:
            delete_list.append(meme_id)
            with allure.step(f'Добавлен мем с ID {meme_id} в список на удаление'):
                pass

    yield add_meme_id

    with allure.step(f'Очистка: удаляем {len(delete_list)} мем(ов)'):
        for meme_id in delete_list:
            with allure.step(f'Удаляем мем с ID {meme_id}'):
                try:
                    meme_endpoint.delete_meme(meme_id)
                except Exception as e:
                    allure.attach(
                        f'Ошибка при удалении мема {meme_id}: {e}',
                        name=f'Cleanup error for ID {meme_id}',
                        attachment_type=allure.attachment_type.TEXT
                    )
