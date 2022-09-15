# c1_eda_frequency_tables

## Issues
- How to get question text?
- What info (overall and on question lvl) is needed?
- What is the meaning of the minor question types (type_minor)?
- for multiple choice questions:
    - is the value always either yes or not chosen? 
    - If the above is the case, is a dict with the subquestions as keys that doesnt display value labels enough?
- Is it ok to use q_response_labelled_en_v1 instead of q_response_v1?
    - q_response_labelled_en_v1 doesnt contain NAs, q_response_v1 does
    - numerical questions are not in q_response_labelled_en_v1

Could make sense to use github issues for this but too lazy atm, will do that later


## Development setup

1. Install poetry
    
    Follow the [official instructions](https://python-poetry.org/docs/)

2. Install requirements

    ```
    poetry install
    ```

3. Create .env file
    The database credentials are provided in evironment variables. 

    ```
    echo "echo "POSTGRES_URL='postgresql://api:1234@localhost:5432/main' \nREDIS_ADR='localhost' \nREDIS_PORT=6379" > .env " > .env
    ```

4. Run app
    ```
    poetry run start
    ```

5. Access App under http://0.0.0.0:8000

4. Access API doc under http://0.0.0.0:8000/docs

## Docker Dev Setup

1. Set up a local container registry
2. Build and tag the image 
    ```
    docker build -t localhost:5000/c1_eda_frequency_api:latest .l
    ```
3. Push the image to the local container registry
    ```
    docker push localhost:5000/c1_eda_frequency_api:latest
    ```
3. Run docker compose
    ```
    docker compose up --build --force-recreate -d
    ```
4. Access the API with e.g. http://0.0.0.0:3000/n_question/q2


## Project explanation
```
├── Dockerfile ---------- Used for container setup
├── eda_frequency_api ---------- All python code aka the package
│   ├── database.py ---------- Establishs connection to the db
│   ├── helpers.py ---------- Helpercode
│   ├── cache.py ---------- Establish connection to the Redis db used as cache
│   ├── main.py ---------- Entrypoint, define routes and settings here
│   ├── models.py ---------- Automatically generated db model, see generate_model()
│   ├── queries.py ---------- All db queries
│   └── schemas.py ---------- All response schemas
├── pyproject.toml ---------- Information for poetry
└── tests ---------- TBA
    ├── __init__.py
    └── test_eda_frequency_api.py
```

## Developments Tips
- FastAPI has a very good [documentation](https://fastapi.tiangolo.com/). 
 


## Sources
- https://realpython.com/python-redis/
- https://docs.sqlalchemy.org/en/14/tutorial/data.html#tutorial-working-with-data
- https://fastapi.tiangolo.com/tutorial/sql-databases/
- https://fastapi.tiangolo.com/advanced/async-sql-databases/
- https://www.tutlinks.com/fastapi-with-postgresql-crud-async/
- https://python.plainenglish.io/how-to-build-a-rest-api-endpoint-on-top-of-an-existing-legacy-database-using-fastapi-489f38feab98
- https://stackoverflow.com/questions/28788186/how-to-run-sqlacodegen
- https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry
- https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker?answertab=modifieddesc#tab-top
- https://fastapi.tiangolo.com/deployment/docker/