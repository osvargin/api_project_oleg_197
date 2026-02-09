import allure
import pytest

from utils.body_data import generate_meme_data, get_case


@allure.feature('Мемы API')
@allure.story('Операции POST (создание мемов)')
class TestCreateMemes:

    @allure.title('Добавление нового мема')
    @pytest.mark.positive
    @pytest.mark.critical
    def test_create_meme(self, meme_endpoint, delete_meme):
        data = generate_meme_data()
        created_id = None

        with allure.step('Отправка запроса на создание мема'):
            meme_endpoint.create_meme(data)
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

        delete_meme(created_id)

    @allure.title('Создание мема с экстра полем')
    @pytest.mark.negative
    @pytest.mark.critical
    def test_create_meme_with_extra_field(self, meme_endpoint, delete_meme):
        data = get_case(extra_field={'extra_field': 'should not be here'})
        with allure.step('Отправка запроса на создание мема'):
            meme_endpoint.create_meme(data)
            created_id = meme_endpoint.meme_id
            delete_meme(created_id) # Добавил фикстуру удаления, так как мем создается
            with allure.step(f'Проверка создания мема с ID: {created_id}'):
                assert created_id is None, 'Мем не должен создаться'

    @allure.title('Создание мема с неполной data')
    @pytest.mark.negative
    @pytest.mark.critical
    def test_create_meme_with_remove_field(self, meme_endpoint):
        data = get_case(remove_field='url')
        with allure.step('Отправка запроса на создание мема'):
            meme_endpoint.create_meme(data)
            created_id = meme_endpoint.meme_id
            assert created_id is None, 'Мем не должен создаться'
