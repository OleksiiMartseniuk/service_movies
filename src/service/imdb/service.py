import os
from datetime import datetime

from src.config import settings
from src.service.imdb.collection_table import ServiceDBIMDB
from src.service.imdb.imdb_api import ClientIMDB
from src.service.imdb.write_file import ServiceJsonWrite


def collection_data() -> None:
    client = ClientIMDB(settings.GROUPS_LIST)
    writer = ServiceJsonWrite(path_group=settings.PATH_GROUP_FILE,
                              path_movies=settings.PATH_MOVIES_FILE)

    db = ServiceDBIMDB(dbname=settings.NAME_DB,
                       user=settings.USER_DB,
                       password=settings.PASSWORD_DB,
                       host=settings.HOST_DB,
                       port=settings.PORT_DB,
                       path_movies=settings.PATH_MOVIES_FILE,
                       group_list=settings.GROUPS_LIST)
    print('init     Generate  database')
    print('delete   Delete data database')
    x = input('Enter the command: ')
    if x == 'init':
        if not os.path.exists(settings.PATH_MOVIES_FILE) and not os.path.exists(settings.PATH_GROUP_FILE):
            res = client.user_count()
            extension_user_count(res, client, writer)
        print('Recording started please wait...')
        start = datetime.now()
        db.write_table()
        stop = datetime.now()
        time = stop - start
        print('Done')
        print(f'Time -> {time}')
    elif x == 'delete':
        print('Removal started please wait...')
        db.delete_tables()
        print('Done')
    else:
        print('Invalid command!')


def extension_user_count(res: dict, client: ClientIMDB, writer: ServiceJsonWrite):
    # Prem акаунт imdb
    if res['maximum'] > 500:
        # Запись групи 250 Top в файл
        data_groups = client.collection_data()
        writer.write_file_group(data_groups)
        print('File "group_movies.json" created')
        print(f'Path {settings.PATH_GROUP_FILE}')
        # Подробная запись фильма из записаной групы
        writer.write_file_movie_test(client)
        print('File "movies.json" created')
        print(f'Path {settings.PATH_MOVIES_FILE}')
    # Free акаунт imdb
    else:
        # Запись групи 250 Top в файл
        data_groups = client.collection_data()
        writer.write_file_group(data_groups)
        print('File "group_movies.json" created')
        print(f'Path {settings.PATH_GROUP_FILE}')

        count = res["maximum"] - res["count"]
        print('Free account imdb')
        print(f'request count: {count}')
        start = int(input('Enter start: '))
        stop = int(input('Enter stop: '))
        if stop - start < count / 2:
            # Подробная запись фильма из записаной групы c интервалом start - stop
            writer.before_recording(client, star=start, stop=stop)
            print('File "movies.json" created')
            print(f'Path {settings.PATH_MOVIES_FILE}')
        else:
            raise ValueError(f'Invalid stop + stop max={count / 2}')
