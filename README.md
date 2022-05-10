# Service Movie
<hr>

* Fastapi
* Tortoise
* Postgres
* Pytest
* Sqlite
* Docker

 ## Current features
<hr>

* CRUD
* imdb
  * Data output movie and tv-series
  * Random movie or tv-series
* auth
  * JWT token
  * Create user
* person
  * Data output person
* user
  * Data output user, update
  * Add movie or tv-series to view
  * Delete from view
  * List to view

* Service IMDB 
  * API IMDB
  * Write JSON 
  * Write DataBase
  * Console service
    

# Instructions
<hr>


Clone repository
<br>
`https://github.com/OleksiiMartseniuk/service_movies.git`

#### Create file .env

```
export API_KEY='your api key'

export POSTGRES_DB='movie'
export POSTGRES_USER='username'
export POSTGRES_PASSWORD='password'

export HOST_DB='db'
export PORT_DB='5432'

export SECRET_KEY='create secret key'
```

#### Docker

`docker-compose up --build`
<br>

#### DataBase initialization
`docker-compose exec app python filling_db.py`

#### Run test
`docker-compose exec app pytest src/tests/`



