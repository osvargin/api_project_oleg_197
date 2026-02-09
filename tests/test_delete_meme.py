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
    def test_delete_meme(self, meme_endpoint):
        data = generate_meme_data()
        created_id = None

        try:
            with allure.step('Отправка запроса на создание мема'):
                response = meme_endpoint.create_meme(data)
                created_id = meme_endpoint.meme_id

            with allure.step(f'Проверка созданного мема с ID: {created_id}'):
                assert created_id is not None, "Мем должен иметь ID"
                meme_endpoint.check_body_contains_one_meme()
                meme_endpoint.assert_fields(
                    id=created_id,
                    text=data['text'],
                    url=data['url'],
                    tags=data['tags'],
                    info=data['info']
                )

        finally:
            if created_id:
                with allure.step(f'Очистка: удаляем созданный мем с ID {created_id}'):
                    try:
                        meme_endpoint.delete_meme(created_id)
                    except Exception as e:
                        allure.attach(
                            f'Ошибка при удалении мема {created_id}: {e}',
                            name='Cleanup error',
                            attachment_type=allure.attachment_type.TEXT
                        )

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
