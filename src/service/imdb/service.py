import os
from datetime import datetime

from src.config import settings
from src.service.imdb.collection_table import ServiceDBIMDB
from src.service.imdb.imdb_api import ClientIMDB
from src.service.imdb.write_file import ServiceJsonWrite


def menu() -> None:
    """" Главное меню """
    print('write    Json entry')
    print('init     Generate  database')
    print('delete   Delete data database')


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
    menu()
    x = input('Enter the command: ')
    if x == 'write':
        write(client, writer)
    elif x == 'init':
        init(db) if error_path() else print('Run the command first -> write')
    elif x == 'delete':
        delete(db)
    else:
        raise SyntaxError('Invalid command!')


def write(client: ClientIMDB, writer: ServiceJsonWrite) -> None:
    """ Запись данных в JSON """
    rez = client.user_count()
    maximum, count = rez['maximum'], rez['count']
    # prim account
    if maximum - count > 520:
        # Запись группы 250 Top в файл
        data_groups = client.collection_data()
        writer.write_file_group(data_groups)
        print('File "group_movies.json" created')
        # Подробная запись фильма из списка группы
        writer.write_file_movie(client)
        print('File "movies.json" created')
        print('Done')
    # free account
    else:
        if maximum - count < 10:
            raise ValueError('Not enough service requests.')
        else:
            start = int(input('Enter start: '))
            stop = int(input('Enter stop: '))
            if stop - start > maximum - count:
                raise ValueError('Not enough service requests.')
            if error_path():
                writer.before_recording(client, star=start, stop=stop)
                print('File "movies.json" created')
            else:
                data_groups = client.collection_data()
                writer.write_file_group(data_groups)
                print('File "group_movies.json" created')
                writer.before_recording(client, star=start, stop=stop)
                print('File "movies.json" created')
            print('Done')


def init(db: ServiceDBIMDB) -> None:
    """ Запись данных в BD """
    print('Recording started please wait...')
    start = datetime.now()
    db.write_table()
    db.close_db()
    stop = datetime.now()
    time = stop - start
    print('Done')
    print(f'Time -> {time}')


def delete(db: ServiceDBIMDB) -> None:
    """ Удаления записей з BD """
    print('Removal started please wait...')
    db.delete_tables()
    db.close_db()
    print('Done')


def error_path() -> bool:
    """ Наличия файла """
    if not os.path.exists(settings.PATH_GROUP_FILE) or \
            not os.path.exists(settings.PATH_MOVIES_FILE):
        return False
    if os.stat(settings.PATH_GROUP_FILE).st_size == 0 or \
            os.stat(settings.PATH_MOVIES_FILE).st_size == 0:
        return False
    return True
