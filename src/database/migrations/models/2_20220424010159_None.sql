-- upgrade --
CREATE TABLE IF NOT EXISTS "group" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(20) NOT NULL,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "group" IS 'Група фильмов';
CREATE TABLE IF NOT EXISTS "movie" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "id_movie" VARCHAR(20) NOT NULL,
    "rank" VARCHAR(20) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "full_title" VARCHAR(255) NOT NULL,
    "year" VARCHAR(10) NOT NULL,
    "image" VARCHAR(1000) NOT NULL,
    "crew" VARCHAR(250) NOT NULL,
    "imdb_rating" VARCHAR(100) NOT NULL,
    "imdb_rating_count" VARCHAR(50) NOT NULL,
    "group_id" INT NOT NULL REFERENCES "group" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "movie" IS 'Фильм';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "user" IS 'Модель Пользователя';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
