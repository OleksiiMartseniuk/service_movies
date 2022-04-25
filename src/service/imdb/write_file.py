import json
import os

from src.service.imdb.imdb_api import ClientIMDB
from src.config.settings import DATA_IMDB_DIR


class ServiceJsonWrite:
    def __init__(self, client: ClientIMDB):
        self.client = client
        self.path_group = f'{DATA_IMDB_DIR}/group_movies.json'
        self.path_movies = f'{DATA_IMDB_DIR}/movies.json'

    def write_file_group(self) -> None:
        """ Запись фильмов груп """
        if not os.path.exists(self.path_group):
            data = self.client.collection_data()
            with open(self.path_group, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

    def write_file_movie(self) -> None:
        """ Запись полного описания фильма """
        with open(self.path_group, 'r') as file:
            data_file = json.load(file)
        data = dict()
        for group in data_file.items():
            movie_list = list()
            for item in group[1][:1]:
                movie = self.client.title_movie(item['id'])
                movie['rank'] = item['rank']
                movie_list.append(movie)

            data[group[0]] = movie_list

        with open(self.path_movies, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def before_recording(self) -> None:
        """ Дозапись файла """
        with open(self.path_group, 'r') as file:
            data_file = json.load(file)

        with open(self.path_movies, 'r') as file:
            data = json.load(file)

        for group in data_file.items():
            for item in group[1][26:28]:
                movie = self.client.title_movie(item['id'])
                movie['rank'] = item['rank']
                data[group[0]].append(movie)

        with open(self.path_movies, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


client = ClientIMDB()
a = ServiceJsonWrite(client)
# a.write_file_movie()
a.before_recording()
