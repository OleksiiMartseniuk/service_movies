import psycopg2
from src.config import settings
from src.service.imdb_api import ClientIMDB


class ServiceDBIMDB:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname=settings.NAME_DB,
            user=settings.USER_DB,
            password=settings.PASSWORD_DB,
            host=settings.HOST_DB,
            port=settings.PORT_DB
        )
        self.clientIMDB = ClientIMDB()

    def write_groups(self) -> None:
        """Запись Group"""
        with self.conn as conn:
            with conn.cursor() as cursor:
                for group in settings.GROUPS_LIST:
                    cursor.execute('INSERT INTO "group" (title) VALUES (%s);', (group,))
                conn.commit()

    def write_movie(self) -> None:
        """Запись Movie"""
        with self.conn as conn:
            for group in self.clientIMDB.collection_data().items():
                with conn.cursor() as cursor:
                    cursor.execute('SELECT id FROM "group" WHERE title=%s;', (group[0],))
                    group_id = cursor.fetchone()
                    for item in group[1]:
                        if item.get('Error'):
                            continue
                        cursor.execute(
                            """INSERT INTO "movie" (id_movie, rank, title, full_title, year, image,
                            crew, imdb_rating, imdb_rating_count, group_id) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                            (item['id'], item['rank'], item['title'], item['fullTitle'], item['year'], item['image'],
                             item['crew'], item['imDbRating'], item['imDbRatingCount'], group_id[0]))
                    conn.commit()

    def delete_table(self) -> None:
        """ Очистка таблиць Group and Movie """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM "group";')
                cursor.execute('DELETE FROM "movie";')
        conn.commit()

    def config(self) -> None:
        self.delete_table()
        self.write_groups()
        self.write_movie()
