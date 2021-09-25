# flask-tdd-docker

https://testdriven.io/courses/tdd-flask

## Develop
```
poetry install
flake8 src
black src
isort src
```
It's better to use a pre-commit hook but I can't as I have multiple projects in this repo...

```
docker-compose up
docker-compose exec api pytest -sv "src/tests" --cov=src
docker-compose exec api flask shell
docker-compose exec api python manage.py recreate_db
docker-compose exec api-db psql -U postgres
```

## Notes
* powershell `$env:FLASK_APP = "src/__init__.py"`
