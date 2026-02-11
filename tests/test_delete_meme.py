import allure
import pytest

from src.api.constants import NOT_EXISTING_MEME_ID
from utils.body_data import generate_meme_data


@allure.feature('Мемы API')
@allure.story('Операции DELETE (удаление мемов)')
class TestDeleteMemes:

    @allure.title('Удаление мема')
    @pytest.mark.positive
    @pytest.mark.critical
    def test_delete_meme(self, meme_endpoint, meme_id):
        with allure.step(f'Удаляем мем с ID {meme_id}'):
            meme_endpoint.delete_meme(meme_id)
            meme_endpoint.assert_status_code(200)
        with allure.step(f'Проверяем, что мем с ID {meme_id} удалён'):
            meme_endpoint.get_meme_by_id(meme_id)
            meme_endpoint.assert_status_code(404)

    @allure.title('Удаление мема NOT_EXISTING_MEME_ID')
    @pytest.mark.positive
    @pytest.mark.medium
    def test_not_existing_meme(self, meme_endpoint):
        meme_endpoint.delete_meme(NOT_EXISTING_MEME_ID)
        meme_endpoint.assert_status_code(404)

    @allure.title('Удаление мема без авторизации')
    @pytest.mark.negative
    @pytest.mark.critical
    def test_delete_meme_without_auth(self, meme_endpoint_without_token, meme_id):
        meme_endpoint_without_token.delete_meme(meme_id)
        meme_endpoint_without_token.assert_status_code(401)
