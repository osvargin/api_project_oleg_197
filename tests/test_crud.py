import pytest
import allure

from utils.body_data import get_base_meme


@allure.feature('CRUD тестирование')
@allure.story('Полный жизненный цикл мема')
class TestCRUDMeme:

    def test_crud_meme(self, meme_id, meme_endpoint):
        with allure.step(f'Создание исходного мема с ID {meme_id}'):
            original_response = meme_endpoint.get_meme_by_id(meme_id)
            original_meme = original_response.json()

        with allure.step(f'Получение всех мемов'):
            meme_endpoint.get_all_memes()
            meme_endpoint.assert_status_code()
            meme_endpoint.check_meme_in_list(meme_id)

        with allure.step(f'Получение мема с ID {meme_id}'):
            meme_endpoint.get_meme_by_id(meme_id)
            meme_endpoint.check_body_contains_one_meme()

        with allure.step('Подготовка данных для обновления'):
            updated_data = get_base_meme()
            updated_data['id'] = meme_id

        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code()

        with allure.step(f'Проверка изменений через GET для ID {meme_id}'):
            meme_endpoint.get_meme_by_id(meme_id)
            meme_endpoint.check_body_contains_one_meme()

        with allure.step(f'Удаление мема с ID {meme_id}'):
            meme_endpoint.delete_meme(meme_id)
            meme_endpoint.assert_status_code()

        with allure.step(f'Проверка удаления через GET для ID {meme_id}'):
            meme_endpoint.get_meme_by_id(meme_id)
            meme_endpoint.assert_status_code(404)

        with allure.step(f'Проверка отсутствия в общем списке мемов ID {meme_id}'):
            meme_endpoint.get_all_memes()
            meme_endpoint.check_meme_in_list(meme_id, False)
