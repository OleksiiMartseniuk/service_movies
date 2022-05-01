import json
import pytest
import responses
from src.service.imdb.write_file import ServiceJsonWrite
from src.service.imdb.imdb_api import ClientIMDB
from src.config import settings
from src.tests import conf_json


def write_group_data():
    valid_data = {}
    for group in settings.GROUPS_LIST:
        valid_data[group] = [item for item in conf_json.valid_json_answer_collection_data['items']]
    with open(settings.PATH_GROUP_FILE_TEST, 'w') as file:
        json.dump(valid_data, file, ensure_ascii=False, indent=4)


def test_service_json_read_not_fount():
    client = ClientIMDB(settings.GROUPS_LIST)
    with pytest.raises(FileNotFoundError):
        writer = ServiceJsonWrite('test/',
                                  'test/')
        writer.write_file_movie(client)


def test_service_json_write_file_group():
    valid_data = {}
    for group in settings.GROUPS_LIST:
        valid_data[group] = [item for item in conf_json.valid_json_answer_collection_data['items']]
    writer = ServiceJsonWrite(settings.PATH_GROUP_FILE_TEST,
                              settings.PATH_MOVIES_FILE_TEST)
    writer.write_file_group(valid_data)
    with open(settings.PATH_GROUP_FILE_TEST) as file:
        data = json.load(file)
    assert valid_data == data


@responses.activate
def test_service_json_write_write_file_movie():
    write_group_data()
    responses.add(responses.GET, f'https://imdb-api.com/ru/API/Title/{settings.API_KEY}/string',
                  json=conf_json.valid_json_answer_title_movie, status=200)
    writer = ServiceJsonWrite(settings.PATH_GROUP_FILE_TEST,
                              settings.PATH_MOVIES_FILE_TEST)
    client = ClientIMDB(settings.GROUPS_LIST)
    writer.write_file_movie(client)
    with open(settings.PATH_MOVIES_FILE_TEST) as file:
        data = json.load(file)
    assert conf_json.valid_json_answer_title_movie_group() == data


@responses.activate
def test_service_json_write_before_recording():
    write_group_data()
    responses.add(responses.GET, f'https://imdb-api.com/ru/API/Title/{settings.API_KEY}/string',
                  json=conf_json.valid_json_answer_title_movie, status=200)
    writer = ServiceJsonWrite(settings.PATH_GROUP_FILE_TEST,
                              settings.PATH_MOVIES_FILE_TEST)
    client = ClientIMDB(settings.GROUPS_LIST)
    writer.before_recording(client, 0, 5)
    with open(settings.PATH_MOVIES_FILE_TEST) as file:
        data = json.load(file)
    assert conf_json.valid_json_answer_title_movie_group() == data
