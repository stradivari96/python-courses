# flask-tdd-docker

https://testdriven.io/courses/tdd-flask

## Develop
```
docker-compose up
docker-compose exec api pytest "src/tests"
docker-compose exec api flask shell
docker-compose exec api python manage.py recreate_db
docker-compose exec api-db psql -U postgres
```

## Notes
* powershell `$env:FLASK_APP = "src/__init__.py"`
