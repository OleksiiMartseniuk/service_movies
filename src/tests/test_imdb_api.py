import pytest
import responses
from requests.exceptions import HTTPError, ConnectionError
from src.service.imdb.imdb_api import ClientIMDB
from src.config import settings
from src.tests import conf_json


@responses.activate
def test_web_client_user_count():
    valid_json_answer = {
        "count": 20,
        "maximum": 100,
        "account": "string",
        "expireDate": "string",
        "errorMessage": ""
    }
    responses.add(responses.GET, f'https://imdb-api.com/API/Usage/{settings.API_KEY}',
                  json=valid_json_answer, status=200)
    client = ClientIMDB(settings.GROUPS_LIST)
    rez = client.user_count()
    assert rez == valid_json_answer


@pytest.mark.parametrize('status_code', [400, 300])
@responses.activate
def test_web_client_status_code_http_error(status_code):
    responses.add(responses.GET, f'https://imdb-api.com/API/Usage/{settings.API_KEY}', status=status_code)
    with pytest.raises(HTTPError):
        client = ClientIMDB(settings.GROUPS_LIST)
        client.user_count()


@pytest.mark.parametrize('error_message, api_key', [('Maximum usage (102 of 100 per day)', settings.API_KEY),
                                                    ('Invalid API Key', '99rfsdf9sdf')])
@responses.activate
def test_web_client_status_code_connection_error(error_message, api_key):
    valid_json_answer = {
        "count": 0,
        "maximum": 0,
        "account": None,
        "expireDate": None,
        "errorMessage": error_message
    }
    responses.add(responses.GET, f'https://imdb-api.com/API/Usage/{api_key}',
                  json=valid_json_answer, status=200)
    with pytest.raises(ConnectionError):
        client = ClientIMDB(settings.GROUPS_LIST)
        client.user_count()


@responses.activate
def test_web_client_collection_data():
    responses.add(responses.GET, f'https://imdb-api.com/en/API/{settings.GROUPS_LIST[0]}/{settings.API_KEY}',
                  json=conf_json.valid_json_answer_collection_data, status=200)
    responses.add(responses.GET, f'https://imdb-api.com/en/API/{settings.GROUPS_LIST[1]}/{settings.API_KEY}',
                  json=conf_json.valid_json_answer_collection_data, status=200)
    valid_data = {}
    for group in settings.GROUPS_LIST:
        valid_data[group] = [item for item in conf_json.valid_json_answer_collection_data['items']]
    client = ClientIMDB(settings.GROUPS_LIST)
    data = client.collection_data()
    assert valid_data == data


@responses.activate
def test_web_title_title_movie():
    responses.add(responses.GET, f'https://imdb-api.com/ru/API/Title/{settings.API_KEY}/id-1234',
                  json=conf_json.valid_json_answer_title_movie, status=200)
    client = ClientIMDB(settings.GROUPS_LIST)
    assert client.title_movie('id-1234') == conf_json.valid_json_answer_title_movie
