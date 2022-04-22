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
    "rank" INT NOT NULL,
    "title" VARCHAR(50) NOT NULL,
    "full_title" VARCHAR(100) NOT NULL,
    "year" VARCHAR(10) NOT NULL,
    "image" VARCHAR(1000) NOT NULL,
    "crew" VARCHAR(100) NOT NULL,
    "imDbRating" VARCHAR(100) NOT NULL,
    "imDbRatingCount" INT NOT NULL,
    "group_id" INT NOT NULL REFERENCES "group" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "movie" IS 'Фильм';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
