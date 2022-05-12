import os
from typing import Optional

import psycopg2
import json

from src.service.imdb.utils import memory_cache


class ServiceDBIMDB:
    """ Запись данных в DB """

    def __init__(self, dbname: str, user: str, password: str, host: str,
                 port: str, path_movies: str, group_list: list) -> None:
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

        self.path_movies = path_movies
        self.group_list = group_list

    def _write_group(self) -> None:
        """Запись Group"""
        for group in self.group_list:
            self.cursor.execute('INSERT INTO "group" (title) VALUES (%s);', (group,))
        self.conn.commit()

    @memory_cache
    def _check(self, teble: str, key: str) -> bool:
        """ Проверка на наличие """
        return False

    def _open_file_movie(self) -> Optional[dict]:
        """ Данные файла """
        if os.path.exists(self.path_movies):
            with open(self.path_movies, 'r') as file:
                data_file = json.load(file)
            return data_file
        else:
            raise FileNotFoundError()

    def _write_four_table(self, genre_list: list, table: str, colum: list,
                          key: str = 'key', value: str = 'value') -> None:
        """ Запись Genre or Сountry or Company or Language """
        for item in genre_list:
            if self._check(table, item[f'{key}']):
                self.cursor.execute(f'INSERT INTO "{table}" ({colum[0]}, {colum[1]}) VALUES (%s, %s);',
                                    (item[f'{key}'], item[f'{value}']))
                self.conn.commit()

    def _write_box_office(self, box_office: dict, id_movie: str) -> None:
        """ Запись BoxOffice"""
        self.cursor.execute("""INSERT INTO "boxoffice" (id_movie, budget, opening_weekend_usa, gross_usa,
                            cumulative_worldwide_gross) VALUES (%s, %s, %s, %s, %s);""",
                            (id_movie,
                             box_office.get('budget'),
                             box_office.get('openingWeekendUSA'),
                             box_office.get('grossUSA'),
                             box_office.get('cumulativeWorldwideGross')))
        self.conn.commit()

    def _write_person(self, list_person: list) -> None:
        """ Запись Person"""
        for item_list in list_person:
            for item in item_list:
                if self._check('person', item['id']):
                    self.cursor.execute("""INSERT INTO "person" (id_person, name, image,
                                        as_character) VALUES (%s, %s, %s, %s);""",
                                        (item['id'], item['name'], item.get('image'), item.get('asCharacter')))
                    self.conn.commit()

    def _write_film_reel(self, film_reel: dict) -> None:
        """ Запись FilmReel"""
        if film_reel['type'] == 'Movie':
            self.cursor.execute(f'SELECT id FROM "group" WHERE title=%s;',
                                ('Top250Movies',))
            id_group = self.cursor.fetchone()[0]
            self.cursor.execute(f'SELECT id FROM "boxoffice" WHERE id_movie=%s;',
                                (film_reel['id'],))
            box_office_id = self.cursor.fetchone()[0]

        if film_reel['type'] == 'TVSeries':
            self.cursor.execute(f'SELECT id FROM "group" WHERE title=%s;',
                                ('Top250TVs',))
            id_group = self.cursor.fetchone()[0]
            box_office_id = None

        if self._check('filmreel', film_reel['id']):
            self.cursor.execute("""INSERT INTO "filmreel" (id_movie, title, full_title, type, year, image,
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
            self.conn.commit()

    def _write_m2m(self, data: list, table: str, table_key: str, search_key: str,
                   film_reel: str, fields: list, key: str):
        """ Запись М2М """
        for item in data:
            self.cursor.execute(f'SELECT id FROM "{table_key}" WHERE {search_key}=%s;', (item[f'{key}'],))
            id_key = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT id FROM "filmreel" WHERE id_movie=%s;', (film_reel,))
            id_movie = self.cursor.fetchone()[0]

            self.cursor.execute(f"""INSERT INTO "{table}"
                            ({fields[0]}, {fields[1]}) VALUES (%s, %s);""",
                                (id_movie, id_key))
        self.conn.commit()

    def write_table(self) -> None:
        # Запись Group
        self._write_group()
        data_file = self._open_file_movie()
        for group in data_file.items():
            list_person = list()
            for item in group[1]:
                # Запись Genre
                self._write_four_table(item['genreList'], 'genre', colum=['title_key', 'title_value'])
                # Запись Country
                self._write_four_table(item['countryList'], 'country', colum=['name_key', 'name_value'])
                # Запись Language
                self._write_four_table(item['languageList'], 'language', colum=['name_key', 'name_value'])
                # Запись Company
                self._write_four_table(item['companyList'], 'company', colum=['id_company', 'name'], key='id', value='name')

                if group[0] == self.group_list[0]:
                    # Запись BoxOffice
                    self._write_box_office(item['boxOffice'], item['id'])

                if item.get('tvSeriesInfo'):
                    list_person.append(item['tvSeriesInfo']['creatorList'])
                if item['directorList'] or item['writerList']:
                    list_person.append(item['directorList'])
                    list_person.append(item['writerList'])
                list_person.append(item['starList'])
                list_person.append(item['actorList'])
                # Запись Person
                self._write_person(list_person)
                # Запись FilmReel
                self._write_film_reel(item)

                if item.get('tvSeriesInfo'):
                    # Запись M2M filmreel_person_creator
                    self._write_m2m(item['tvSeriesInfo']['creatorList'], 'filmreel_person_creator', 'person',
                                    'id_person', item['id'], ['filmreel_id', 'person_id'], 'id')
                # Запись M2M filmreel_person_star
                self._write_m2m(item['starList'], 'filmreel_person_star', 'person', 'id_person',
                                item['id'], ['filmreel_id', 'person_id'], 'id')
                # Запись M2M filmreel_person_actor
                self._write_m2m(item['actorList'], 'filmreel_person_actor', 'person', 'id_person',
                                item['id'], ['filmreel_id', 'person_id'], 'id')
                if item['directorList'] or item['writerList']:
                    # Запись M2M filmreel_person_director
                    self._write_m2m(item['directorList'], 'filmreel_person_director', 'person',
                                    'id_person', item['id'], ['filmreel_id', 'person_id'], 'id')
                    # Запись M2M filmreel_person_writer
                    self._write_m2m(item['writerList'], 'filmreel_person_writer', 'person', 'id_person',
                                    item['id'], ['filmreel_id', 'person_id'], 'id')
                # Запись M2M filmreel_company
                self._write_m2m(item['companyList'], 'filmreel_company', 'company', 'id_company',
                                item['id'], ['filmreel_id', 'company_id'], 'id')
                # Запись M2M filmreel_country
                self._write_m2m(item['countryList'], 'filmreel_country', 'country', 'name_key',
                                item['id'], ['filmreel_id', 'country_id'], 'key')
                # Запись M2M filmreel_genre
                self._write_m2m(item['genreList'], 'filmreel_genre', 'genre', 'title_key',
                                item['id'], ['filmreel_id', 'genre_id'], 'key')
                # Запись M2M filmreel_language
                self._write_m2m(item['languageList'], 'filmreel_language', 'language', 'name_key',
                                item['id'], ['filmreel_id', 'language_id'], 'key')
        self._close_db()

    def delete_tables(self, tables_list) -> None:
        """ Очистка таблиць """
        for table in tables_list:
            self.cursor.execute(f'DELETE FROM "{table}";')
        self.conn.commit()
        self._close_db()

    def _close_db(self) -> None:
        """ Закрыть соединение"""
        self.cursor.close()
        self.conn.close()
