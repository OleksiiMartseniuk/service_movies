import requests
from requests.exceptions import HTTPError, ConnectionError

from src.config.settings import API_KEY
from urllib.parse import urljoin


class ClientIMDB:
    """ Клиент IMDB"""
    def __init__(self, groups: list, api_key: str = API_KEY, domain: str = 'https://imdb-api.com') -> None:
        self.api_key = api_key
        self.domain = domain
        self.groups = groups

    def _get(self, url_part: str) -> dict:
        url = urljoin(self.domain, url_part)
        response = requests.get(url)
        if response.status_code == 200:
            if not response.json().get('errorMessage'):
                return response.json()
            else:
                raise ConnectionError(response.json().get('errorMessage'))
        raise HTTPError(f'status_code -> {response.status_code}')

    def collection_data(self) -> dict:
        """ Сбор данных по групам """
        data = dict()
        for group_title in self.groups:
            url_part = f'/en/API/{group_title}/{self.api_key}'
            response = self._get(url_part)
            data[f'{group_title}'] = [item for item in response['items']]
        return data

    def title_movie(self, id: str) -> dict:
        """ Полные данные фильма """
        url_part = f'/ru/API/Title/{self.api_key}/{id}'
        response = self._get(url_part)
        return response

    def user_count(self):
        """ Количество запросов """
        url_part = f'/API/Usage/{self.api_key}'
        response = self._get(url_part)
        return response
