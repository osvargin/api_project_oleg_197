import allure
import requests
from src.api.base_api import BaseApi
from src.api.constants import BASE_URL, MEME_PATH


class MemeEndpoint(BaseApi):
    url = BASE_URL + MEME_PATH

    @allure.step('GET /meme - Получение всех мемов')
    def get_all_memes(self):
        self.response = requests.get(self.url, headers=self.headers)
        return self.response

    @allure.step('GET /meme/ - Получение мема по ID: {meme_id}')
    def get_meme_by_id(self, meme_id):
        self.response = requests.get(f'{self.url}/{meme_id}', headers=self.headers)
        return self.response

    @allure.step('POST /meme - Создание нового мема')
    def create_meme(self, data):
        self.response = requests.post(self.url, json=data, headers=self.headers)
        if self.response.status_code == 200:
            self.meme_id = self.response.json()["id"]
        else:
            self.meme_id = None
        return self.response

    @allure.step('PUT /meme/ - Обновление мема с ID: {meme_id}')
    def update_meme(self, meme_id, data):
        self.response = requests.put(f'{self.url}/{meme_id}', json=data, headers=self.headers)
        return self.response

    @allure.step('DELETE /meme/- Удаление мема с ID: {meme_id}')
    def delete_meme(self, meme_id):
        self.response = requests.delete(f'{self.url}/{meme_id}', headers=self.headers)
        return self.response