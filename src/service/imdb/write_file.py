import json
import os

from src.service.imdb.imdb_api import ClientIMDB


class ServiceJsonWrite:
    """ Запись даных в json """

    def __init__(self, path_group: str, path_movies: str) -> None:
        self.path_group = path_group
        self.path_movies = path_movies

    def _open_write(self, data: dict, path: str) -> None:
        with open(path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _open_read(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError

    def write_file_group(self, data: dict) -> None:
        """ Запись фильмов груп """
        self._open_write(data, self.path_group)

    def write_file_movie(self, client: ClientIMDB) -> None:
        """ Запись полного описания фильма """
        data_file = self._open_read(self.path_group)
        data = dict()
        for group in data_file.items():
            movie_list = list()
            for item in group[1]:
                movie = client.title_movie(item['id'])
                movie['rank'] = item['rank']
                movie_list.append(movie)

            data[group[0]] = movie_list

        self._open_write(data, self.path_movies)

    def before_recording(self, client: ClientIMDB, star: int, stop: int) -> None:
        """ Дозапись файла """
        data_file = self._open_read(self.path_group)
        if not os.path.exists(self.path_movies):
            open(self.path_movies, 'w').close()
            data = {}
        else:
            data = self._open_read(self.path_movies)

        for group in data_file.items():
            for item in group[1][star:stop]:
                movie = client.title_movie(item['id'])
                movie['rank'] = item['rank']
                data[group[0]].append(movie)

        self._open_write(data, self.path_movies)
