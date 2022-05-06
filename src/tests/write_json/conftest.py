import pytest
import os
from src.config import settings


@pytest.fixture(autouse=True)
def clear_file():
    if os.path.exists(settings.PATH_MOVIES_FILE_TEST):
        open(settings.PATH_MOVIES_FILE_TEST, 'w').close()
    if os.path.exists(settings.PATH_GROUP_FILE_TEST):
        open(settings.PATH_GROUP_FILE_TEST, 'w').close()
