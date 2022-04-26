import json
import os

from src.service.imdb.imdb_api import ClientIMDB
from src.config import settings


class ServiceJsonWrite:
    def __init__(self, client: ClientIMDB, path_group: str, path_movies: str):
        self.client = client
        self.path_group = path_group
        self.path_movies = path_movies

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
            for item in group[1][28:78]:
                movie = self.client.title_movie(item['id'])
                movie['rank'] = item['rank']
                data[group[0]].append(movie)

        with open(self.path_movies, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


client = ClientIMDB()
a = ServiceJsonWrite(client=client,
                     path_group=settings.PATH_GROUP_FILE,
                     path_movies=settings.PATH_MOVIES_FILE)

# a.before_recording()
