import allure
import pytest

from utils.body_data import get_base_meme, prepare_update_data


@allure.feature('Мемы API')
@allure.story('Операции PUT (обновление мемов)')
class TestUpdateMemes:

    @allure.title('Обновление мема')
    @pytest.mark.positive
    @pytest.mark.critical
    def test_update_meme(self, meme_endpoint, meme_id):
        with allure.step(f'Получение исходного мема с ID {meme_id}'):
            pass

        with allure.step('Подготовка данных для обновления'):
            updated_data = get_base_meme()
            updated_data['id'] = meme_id

        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code()

        with allure.step(f'Получение обновлённого мема с ID {meme_id}'):
            meme_endpoint.get_meme_by_id(meme_id)

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

    @allure.title('Обновление мема с отсутствующим полем "{field}"')
    @pytest.mark.parametrize('field', ['text', 'url', 'tags', 'info'])
    @pytest.mark.negative
    @pytest.mark.medium
    def test_update_meme_missing_required_field(self, meme_endpoint, meme_id, field):
        with allure.step(f'Подготовка данных без поля "{field}"'):
            updated_data = get_base_meme()
            updated_data['id'] = meme_id
            del updated_data[field]

        with allure.step(f'Обновления мема с отсутствующим полем "{field}"'):
            meme_endpoint.update_meme(meme_id, updated_data)
        with allure.step(f'Проверка выполнения обновления мема с отсутствующим полем'):
            meme_endpoint.assert_status_code(400)

    @allure.title('Обновление с невалидным полем ID: "{id}"')
    @pytest.mark.parametrize('id',
                             (
                                     99999999999999999, 0, -1,
                                     ['test', 'meme', 'text'], 'three',
                                     {'color': ['white', 'black'], 'objects': ['cat', 'text', 'hands']},
                                     None, True)
                             )
    @pytest.mark.negative
    @pytest.mark.medium
    def test_update_meme_with_invalid_id(self, meme_endpoint, meme_id, id):
        with allure.step('Подготовка данных для обновления'):
            updated_data = prepare_update_data(meme_id, id=id)
        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code(400)

    @allure.title('Обновление мема с невалидным полем text: "{text}"')
    @pytest.mark.parametrize('text',
                             (
                                     123, ['test', 'meme', 'text'], False,
                                     {'color': ['white', 'black'], 'objects': ['cat', 'text', 'hands']},
                                     None)
                             )
    @pytest.mark.negative
    @pytest.mark.medium
    def test_update_meme_with_invalid_text(self, meme_endpoint, meme_id, text):
        with allure.step('Подготовка данных для обновления'):
            updated_data = prepare_update_data(meme_id, text=text)
        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code(400)

    @allure.title('Обновление мема с невалидным полем url: "{url}"')
    @pytest.mark.parametrize('url',
                             (
                                     123, ['test', 'meme', 'text'], False,
                                     {'color': ['white', 'black'], 'objects': ['cat', 'text', 'hands']},
                                     None)
                             )
    @pytest.mark.negative
    @pytest.mark.medium
    def test_update_meme_with_invalid_url(self, meme_endpoint, meme_id, url):
        with allure.step('Подготовка данных для обновления'):
            updated_data = prepare_update_data(meme_id, url=url)
        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code(400)

    @allure.title('Обновление мема с невалидным полем tags: "{tags}"')
    @pytest.mark.parametrize('tags',
                             (
                                     123, False,
                                     {'color': ['white', 'black'], 'objects': ['cat', 'text', 'hands']},
                                     None)
                             )
    @pytest.mark.negative
    @pytest.mark.medium
    def test_update_meme_with_invalid_tags(self, meme_endpoint, meme_id, tags):
        with allure.step('Подготовка данных для обновления'):
            updated_data = prepare_update_data(meme_id, tags=tags)
        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code(400)

    @allure.title('Обновление мема с невалидным полем info: "{info}"')
    @pytest.mark.parametrize('info',
                             (
                                     123, False, ['test', 'meme', 'text'],
                                     None)
                             )
    @pytest.mark.negative
    @pytest.mark.medium
    def test_update_meme_with_invalid_info(self, meme_endpoint, meme_id, info):
        with allure.step('Подготовка данных для обновления'):
            updated_data = prepare_update_data(meme_id, info=info)
        with allure.step('Отправка запроса на обновление мема'):
            meme_endpoint.update_meme(meme_id, updated_data)
            meme_endpoint.assert_status_code(400)
