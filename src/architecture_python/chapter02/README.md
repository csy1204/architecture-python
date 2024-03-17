
## Run

```sh
uvicorn src.architecture_python.chapter02.main:app --reload
```

## Test

```sh
pytest tests/chapter02
```

## Trouble Shooting

```log
sqlalchemy.exc.InvalidRequestError: The 'sqlalchemy.orm.mapper()' function is removed as of SQLAlchemy 2.0.  Use the 'sqlalchemy.orm.registry.map_imperatively()` method of the ``sqlalchemy.orm.registry`` class to perform classical mapping.
```
