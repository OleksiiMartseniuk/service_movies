import psycopg2
import json
from src.config import settings
from src.service.imdb.imdb_api import ClientIMDB


class ServiceDBIMDB:
    def __init__(
            self,
            client: ClientIMDB,
            dbname: str,
            user: str,
            password: str,
            host: str,
            port: str,
            path_movies: str
    ) -> None:
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.clientIMDB = client
        self.path_movies = path_movies

    def write_group(self) -> None:
        """Запись Group"""
        with self.conn as conn:
            with conn.cursor() as cursor:
                for group in settings.GROUPS_LIST:
                    cursor.execute('SELECT id FROM "group" WHERE title=%s;', (group,))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO "group" (title) VALUES (%s);', (group,))
                        conn.commit()

    def _open_file_movie(self) -> dict:
        """ Данные файла """
        with open(self.path_movies, 'r') as file:
            data_file = json.load(file)
        return data_file

    def write_four_table(self, genre_list: list, table: str, colum: list) -> None:
        """ Запись Genre or Сountry or Company or Language """
        with self.conn as conn:
            with conn.cursor() as cursor:
                for item in genre_list:
                    cursor.execute(f'SELECT id FROM "{table}" WHERE {colum[0]}=%s;',
                                   (item.get('key') or item.get('id'),))
                    if not cursor.fetchone():
                        cursor.execute(f'INSERT INTO "{table}" ({colum[0]}, {colum[1]}) VALUES (%s, %s);',
                                       (item.get('key') or item.get('id'), item.get('value') or item.get('name')))
                        conn.commit()

    def write_box_office(self, box_office: dict, id_movie: str) -> None:
        """ Запись BoxOffice"""
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT id FROM "boxoffice" WHERE id_movie=%s;',
                               (id_movie,))
                if not cursor.fetchone():
                    cursor.execute("""INSERT INTO "boxoffice" (id_movie, budget, opening_weekend_usa, gross_usa, 
                                   cumulative_worldwide_gross) VALUES (%s, %s, %s, %s, %s);""",
                                   (id_movie,
                                    box_office.get('budget'),
                                    box_office.get('openingWeekendUSA'),
                                    box_office.get('grossUSA'),
                                    box_office.get('cumulativeWorldwideGross')))
                    conn.commit()

    def write_person(self, list_person: list) -> None:
        """ Запись Person"""
        with self.conn as conn:
            with conn.cursor() as cursor:
                for item_list in list_person:
                    for item in item_list:
                        cursor.execute('SELECT id FROM "person" WHERE id_person=%s;', (item['id'],))
                        if not cursor.fetchone():
                            cursor.execute("""INSERT INTO "person" (id_person, name, image,
                                            as_character) VALUES (%s, %s, %s, %s);""",
                                           (item['id'], item['name'], item.get('image'), item.get('asCharacter')))
                            conn.commit()

    def write_film_reel(self, film_reel: dict) -> None:
        """ Запись FilmReel"""
        with self.conn as conn:
            with conn.cursor() as cursor:
                if film_reel['type'] == 'Movie':
                    cursor.execute(f'SELECT id FROM "group" WHERE title=%s;',
                                   ('Top250Movies',))
                    id_group = cursor.fetchone()[0]
                    cursor.execute(f'SELECT id FROM "boxoffice" WHERE id_movie=%s;',
                                   (film_reel['id'],))
                    box_office_id = cursor.fetchone()[0]

                if film_reel['type'] == 'TVSeries':
                    cursor.execute(f'SELECT id FROM "group" WHERE title=%s;',
                                   ('Top250TVs',))
                    id_group = cursor.fetchone()[0]
                    box_office_id = None

                cursor.execute(f'SELECT id FROM "filmreel" WHERE id_movie=%s;',
                               (film_reel['id'],))
                if not cursor.fetchone():
                    cursor.execute("""INSERT INTO "filmreel" (id_movie, title, full_title, type, year, image,
                                    release_date, runtime_min, runtime_str, plot, plot_local, plot_local_is_rtl,
                                    awards, content_rating, imdb_rating, imDd_rating_votes, metacritic_rating,
                                    tagline, rank_top_250, group_id, box_office_id) VALUES (%s, %s, %s, %s, %s, %s, %s,
                                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                                   (film_reel['id'], film_reel['title'], film_reel['fullTitle'], film_reel['type'],
                                    film_reel['year'], film_reel['image'], film_reel['releaseDate'],
                                    film_reel.get('runtimeMins'), film_reel.get('runtimeStr'), film_reel['plot'],
                                    film_reel['plotLocal'], film_reel['plotLocalIsRtl'], film_reel['awards'],
                                    film_reel['contentRating'], film_reel['imDbRating'], film_reel['imDbRatingVotes'],
                                    film_reel['metacriticRating'], film_reel['tagline'], film_reel['rank'],
                                    id_group, box_office_id))
                    conn.commit()

    def write_m2m_person(self, data: list, table: str, film_reel: str) -> None:
        """ Запись М2М FilmReel is Person"""
        with self.conn as conn:
            with conn.cursor() as cursor:
                for item in data:
                    cursor.execute('SELECT id FROM "person" WHERE id_person=%s;', (item['id'],))
                    id_person = cursor.fetchone()[0]
                    cursor.execute('SELECT id FROM "filmreel" WHERE id_movie=%s;', (film_reel,))
                    id_movie = cursor.fetchone()[0]

                    cursor.execute(f"""INSERT INTO "{table}"
                                    (filmreel_id, person_id) VALUES (%s, %s);""",
                                   (id_movie, id_person))
                    conn.commit()

    def write_m2m(self, data: list, table: str, film_reel: str):
        """"""
        pass

    def write_table(self) -> None:
        # Запись Group
        # self.write_group()
        data_file = self._open_file_movie()
        for group in data_file.items():
            list_person = list()
            for item in group[1]:
                # # Запись Genre
                # self.write_four_table(item['genreList'], 'genre', colum=['title_key', 'title_value'])
                # # Запись Country
                # self.write_four_table(item['countryList'], 'country', colum=['name_key', 'name_value'])
                # # Запись Language
                # self.write_four_table(item['languageList'], 'language', colum=['name_key', 'name_value'])
                # # Запись Company
                # self.write_four_table(item['companyList'], 'company', colum=['id_company', 'name'])
                #
                # if group[0] == settings.GROUPS_LIST[0]:
                #     # Запись BoxOffice
                #     self.write_box_office(item['boxOffice'], item['id'])
                #
                # if item.get('tvSeriesInfo'):
                #     list_person.append(item['tvSeriesInfo']['creatorList'])
                # if item['directorList'] or item['writerList']:
                #     list_person.append(item['directorList'])
                #     list_person.append(item['writerList'])
                # list_person.append(item['starList'])
                # list_person.append(item['actorList'])
                # # Запись Person
                # self.write_person(list_person)
                # # Запись FilmReel
                # self.write_film_reel(item)

                # Запись М2М FilmReel is Person
                # if item.get('tvSeriesInfo'):
                #     self.write_m2m_person(item['tvSeriesInfo']['creatorList'], 'filmreel_person_creator', item['id'])
                # self.write_m2m_person(item['starList'], 'filmreel_person_star', item['id'])
                # self.write_m2m_person(item['actorList'], 'filmreel_person_actor', item['id'])
                # self.write_m2m_person(item['creatorList'], 'filmreel_person_creator', item['id'])
                # if item['directorList'] or item['writerList']:
                #     self.write_m2m_person(item['directorList'], 'filmreel_person_director', item['id'])
                #     self.write_m2m_person(item['writerList'], 'filmreel_person_writer', item['id'])

                pass

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
                cursor.execute('DELETE FROM "filmreel";')
                # cursor.execute('DELETE FROM "movie";')
        conn.commit()

    def config(self) -> None:
        self.delete_table()
        self.write_groups()
        self.write_movie()


client = ClientIMDB()
db = ServiceDBIMDB(client=client,
                   dbname=settings.NAME_DB,
                   user=settings.USER_DB,
                   password=settings.PASSWORD_DB,
                   host=settings.HOST_DB,
                   port=settings.PORT_DB,
                   path_movies=settings.PATH_MOVIES_FILE)

db.write_table()
# db.delete_table()

