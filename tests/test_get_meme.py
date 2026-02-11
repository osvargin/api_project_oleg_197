import allure
import pytest

from src.api.constants import NOT_EXISTING_MEME_ID


@allure.feature('Мемы API')
@allure.story('Операции GET (получение мемов)')
class TestGetMemes:

    @allure.title('Получение всех мемов')
    @pytest.mark.positive
    @pytest.mark.critical
    def test_get_all_memes(self, meme_endpoint):
        meme_endpoint.get_all_memes()
        meme_endpoint.assert_status_code()
        meme_endpoint.check_body_contains_memes()

    @allure.title('Получение конкретного мема по ID')
    @pytest.mark.positive
    @pytest.mark.medium
    def test_get_meme_by_id(self, meme_endpoint, meme_id):
        with allure.step(f'Получение мема с ID {meme_id}'):
            meme_endpoint.get_meme_by_id(meme_id)
            meme_endpoint.check_body_contains_one_meme()
            meme_endpoint.check_meme_has_correct_id(meme_id)

    @allure.title('Получение конкретного мема по NOT_EXISTING_MEME_ID')
    @pytest.mark.negative
    @pytest.mark.medium
    def test_get_meme_by_not_exist_meme(self, meme_endpoint):
        meme_endpoint.get_meme_by_id(NOT_EXISTING_MEME_ID)
        meme_endpoint.assert_status_code(404)

    @allure.title('Получение мема без авторизации')
    @pytest.mark.negative
    @pytest.mark.critical
    def test_without_auth(self, meme_endpoint_without_token, meme_id):
        meme_endpoint_without_token.get_meme_by_id(meme_id)
        meme_endpoint_without_token.assert_status_code(401)
