import json
import pytest

from src.config import settings
from src.tests import conf_json


@pytest.fixture
def create_file(tmp_path) -> tuple:
    path_groups = tmp_path / 'groups.json'
    path_movies = tmp_path / 'movies.json'
    return path_groups, path_movies


@pytest.fixture
def write_group_data(create_file) -> tuple:
    valid_data = {}
    for group in settings.GROUPS_LIST:
        valid_data[group] = [item for item in conf_json.valid_json_answer_collection_data['items']]
    with open(create_file[0], 'w') as file:
        json.dump(valid_data, file, ensure_ascii=False, indent=4)
    return create_file
