import faker
import allure

from src.api.constants import AUTHORIZATION_HEADER, BASE_URL


class BaseApi:
    fake = faker.Faker()

    def __init__(self):
        # self.url = BASE_URL
        self.response = None
        self.json = None
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.token = None
        self.body = None
        self.meme_id = None

    @allure.step('Проверка статус кода')
    def assert_status_code(self, expected_status=200):
        assert self.response.status_code == expected_status, \
            f'Ожидался статус {expected_status}, получен: {self.response.status_code}'

    @allure.step('Добавляем токен авторизации в headers')
    def set_token(self, token):
        if token:
            self.headers[AUTHORIZATION_HEADER] = token
        elif AUTHORIZATION_HEADER in self.headers:
            del self.headers[AUTHORIZATION_HEADER]

    def create_endpoint_with_token(self, endpoint_class, token):
        endpoint = endpoint_class()
        endpoint.set_token(token)
        return endpoint

    @allure.step('Проверка наличия всех обязательных полей')
    def check_body_contains_memes(self):
        body = self.response.json()
        memes = body.get('data')
        assert isinstance(body, dict)
        for meme in memes:
            assert 'id' in meme
            assert 'text' in meme
            assert 'url' in meme
            assert 'tags' in meme
            assert 'info' in meme

    @allure.step('Проверка наличия всех обязательных полей')
    def check_body_contains_one_meme(self):
        body = self.response.json()
        assert 'id' in body
        assert 'text' in body
        assert 'url' in body
        assert 'tags' in body
        assert 'info' in body

    @allure.step('Проверка ожидаемого поля')
    def assert_fields(self, **expected_fields):
        body = self.response.json()

        if 'data' in body and isinstance(body['data'], dict):
            meme = body['data']
        elif 'result' in body and isinstance(body['result'], dict):
            meme = body['result']
        else:
            meme = body

        failed_checks = []
        for field, expected_value in expected_fields.items():
            actual_value = meme.get(field)

            if actual_value != expected_value:
                error_msg = f'Поле "{field}": ожидалось {expected_value}, получено {actual_value}'
                failed_checks.append(error_msg)
                with allure.step(f'{error_msg}'):
                    pass
            else:
                with allure.step(f'Поле "{field}" совпадает: {expected_value}'):
                    pass

        if failed_checks:
            raise AssertionError('\n'.join(failed_checks))

    @allure.step('Проверка наличия ID мема в общем списке')
    def check_meme_in_list(self, meme_id, should_be_present=True):
        memes = self.response.json().get('data') if isinstance(self.response.json(), dict) else self.json

        assert isinstance(memes, list), 'Ожидался список мемов (ключ "data" или корень JSON)'
        assert len(memes) > 0, 'Список мемов пуст'

        ids = [m.get('id') for m in memes] if memes else []
        if should_be_present:
            assert meme_id in ids, f'Мем с id {meme_id} не найден в списке'
        else:
            assert meme_id not in ids, f'Мем с id {meme_id} всё еще присутствует в списке'

    @allure.step('Проверяем, что мем имеет ожидаемый ID')
    def check_meme_has_correct_id(self, meme_id):
        data = self.response.json()
        actual_id = data.get('id')
        assert actual_id == meme_id
