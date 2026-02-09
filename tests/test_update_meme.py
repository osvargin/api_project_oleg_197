import allure
import pytest

from src.api.constants import NOT_EXISTING_MEME_ID
from utils.body_data import get_base_meme


@allure.feature('Мемы API')
@allure.story('Операции PUT (обновление мемов)')
class TestUpdateMemes:

    @allure.title('Обновление мема')
    @pytest.mark.positive
    @pytest.mark.critical
    def test_update_meme(self, meme_endpoint, meme_id):
        with allure.step(f'Получение исходного мема с ID {meme_id}'):
            original_response = meme_endpoint.get_meme_by_id(meme_id)
            original_meme = original_response.json()

        with allure.step('Подготовка данных для обновления'):
            updated_data = get_base_meme()
            updated_data['id'] = meme_id

        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code()

        with allure.step(f'Получение обновлённого мема с ID {meme_id}'):
            updated_response = meme_endpoint.get_meme_by_id(meme_id)
            updated_meme = updated_response.json()

        with allure.step(f'Проверка обновлённого мема с ID {meme_id}'):
            meme_endpoint.check_body_contains_one_meme()
            expected_id = str(meme_id)
            meme_endpoint.assert_fields(
                id=expected_id,
                text=updated_data['text'],
                url=updated_data['url'],
                tags=updated_data['tags'],
                info=updated_data['info']
            )

        assert updated_meme['text'] == updated_data['text'], \
            f'Текст не обновился. Ожидалось: {updated_data['text']}, получено: {updated_meme['text']}'
        assert updated_meme['url'] == updated_data['url'], \
            f'URL не обновился. Ожидалось: {updated_data['url']}, получено: {updated_meme['url']}'

    @allure.title('Обновление несуществующего мема')
    @pytest.mark.negative
    @pytest.mark.medium
    def test_update_non_existent_meme(self, meme_endpoint):
        with allure.step('Подготовка данных для обновления'):
            updated_data = get_base_meme()
            updated_data['id'] = NOT_EXISTING_MEME_ID
        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(NOT_EXISTING_MEME_ID, updated_data)
            meme_endpoint.assert_status_code(404)

    @allure.title('Обновление мема без авторизации')
    @pytest.mark.negative
    @pytest.mark.critical
    def test_without_auth(self, meme_endpoint_without_token, meme_id):
        with allure.step('Подготовка данных для обновления'):
            update_data = get_base_meme()
            update_data['id'] = meme_id
        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint_without_token.update_meme(meme_id, update_data)
            meme_endpoint_without_token.assert_status_code(401)
