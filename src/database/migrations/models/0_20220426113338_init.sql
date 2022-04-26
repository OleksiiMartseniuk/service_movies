-- upgrade --
CREATE TABLE IF NOT EXISTS "boxoffice" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "budget" VARCHAR(50),
    "opening_weekend_usa" VARCHAR(50),
    "gross_usa" VARCHAR(50),
    "cumulative_worldwide_gross" VARCHAR(50)
);
COMMENT ON TABLE "boxoffice" IS 'Театральная касса ';
CREATE TABLE IF NOT EXISTS "company" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "id_company" VARCHAR(15) NOT NULL,
    "name" VARCHAR(150) NOT NULL
);
COMMENT ON TABLE "company" IS 'Компания ';
CREATE TABLE IF NOT EXISTS "country" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name_key" VARCHAR(50) NOT NULL,
    "name_value" VARCHAR(50) NOT NULL
);
COMMENT ON TABLE "country" IS 'Страна ';
CREATE TABLE IF NOT EXISTS "genre" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title_key" VARCHAR(50) NOT NULL,
    "title_value" VARCHAR(50) NOT NULL
);
COMMENT ON TABLE "genre" IS 'Жанры ';
CREATE TABLE IF NOT EXISTS "group" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(20) NOT NULL,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "group" IS 'Група фильмов';
CREATE TABLE IF NOT EXISTS "filmreel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "id_movie" VARCHAR(20) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "full_title" VARCHAR(255) NOT NULL,
    "type" VARCHAR(20) NOT NULL,
    "year" VARCHAR(10) NOT NULL,
    "image" VARCHAR(1000) NOT NULL,
    "release_date" VARCHAR(10) NOT NULL,
    "runtime_min" VARCHAR(10),
    "runtime_str" VARCHAR(20),
    "plot" TEXT NOT NULL,
    "plot_local" TEXT NOT NULL,
    "plot_local_is_rtl" BOOL NOT NULL,
    "awards" VARCHAR(50) NOT NULL,
    "content_rating" VARCHAR(10) NOT NULL,
    "imdb_rating" VARCHAR(100) NOT NULL,
    "imDd_rating_votes" VARCHAR(20) NOT NULL,
    "metacritic_rating" VARCHAR(10),
    "tagline" VARCHAR(200),
    "rank_top_250" VARCHAR(20) NOT NULL,
    "group_id" INT NOT NULL REFERENCES "group" ("id") ON DELETE CASCADE,
    "box_office_id" INT  UNIQUE REFERENCES "boxoffice" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "filmreel" IS 'Кино лента ';
CREATE TABLE IF NOT EXISTS "language" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name_key" VARCHAR(50) NOT NULL,
    "name_value" VARCHAR(50) NOT NULL
);
COMMENT ON TABLE "language" IS 'Язык ';
CREATE TABLE IF NOT EXISTS "person" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "id_person" VARCHAR(15) NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "image" VARCHAR(1000),
    "as_character" VARCHAR(150)
);
COMMENT ON TABLE "person" IS 'Модель человека ';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "first_name" VARCHAR(100) NOT NULL,
    "last_name" VARCHAR(100) NOT NULL,
    "data_join" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_join" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "user" IS 'Модель Пользователя';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "filmreel_person_actor" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "person_id" INT NOT NULL REFERENCES "person" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_language" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "language_id" INT NOT NULL REFERENCES "language" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_company" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_person_writer" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "person_id" INT NOT NULL REFERENCES "person" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_person_director" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "person_id" INT NOT NULL REFERENCES "person" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_person_star" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "person_id" INT NOT NULL REFERENCES "person" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_person_creator" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "person_id" INT NOT NULL REFERENCES "person" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_country" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "country_id" INT NOT NULL REFERENCES "country" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "filmreel_genre" (
    "filmreel_id" INT NOT NULL REFERENCES "filmreel" ("id") ON DELETE CASCADE,
    "genre_id" INT NOT NULL REFERENCES "genre" ("id") ON DELETE CASCADE
);
