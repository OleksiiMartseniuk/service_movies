import json
import pytest
from src.service.imdb.write_file import ServiceJsonWrite
from src.config import settings
from src.tests import conf_json
from unittest import mock


class TestServiceJsonWrite:

    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_service_json_read_not_fount(self, MockClientIMDB):
        mock_client = MockClientIMDB()
        with pytest.raises(FileNotFoundError):
            writer = ServiceJsonWrite('test/',
                                      'test/')
            writer.write_file_movie(mock_client)

    def test_service_json_write_file_group(self, create_file):
        path_groups, path_movies = create_file
        valid_data = {}
        for group in settings.GROUPS_LIST:
            valid_data[group] = [item for item in conf_json.valid_json_answer_collection_data['items']]
        writer = ServiceJsonWrite(path_groups, path_movies)
        writer.write_file_group(valid_data)

        with open(path_groups) as file:
            data = json.load(file)
        assert valid_data == data

    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_service_json_write_write_file_movie(self, MockClientIMDB, write_group_data):
        path_groups, path_movies = write_group_data

        writer = ServiceJsonWrite(path_groups, path_movies)

        mock_client = MockClientIMDB()
        mock_client.title_movie.return_value = conf_json.valid_json_answer_title_movie

        writer.write_file_movie(mock_client)

        with open(path_movies) as file:
            data = json.load(file)
        assert conf_json.valid_json_answer_title_movie_group() == data

    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_service_json_write_before_recording(self, MockClientIMDB, write_group_data):
        path_groups, path_movies = write_group_data

        writer = ServiceJsonWrite(path_groups, path_movies)

        mock_client = MockClientIMDB()
        mock_client.title_movie.return_value = conf_json.valid_json_answer_title_movie

        writer.before_recording(mock_client, 0, 5)

        with open(path_movies) as file:
            data = json.load(file)
        assert conf_json.valid_json_answer_title_movie_group() == data
