# taxi-react-app
https://testdriven.io/courses/taxi-react

```
$env:PGDATABASE="taxi"
$env:PGUSER="taxi"
$env:PGPASSWORD="taxi"
```

```
docker run --name some-postgres -p 5432:5432 -e POSTGRES_USER=taxi -e POSTGRES_DB=taxi -e POSTGRES_PASSWORD=taxi -d postgres
docker run --name some-redis -p 6379:6379 -d redis
```

```
python manage.py runserver
python manage.py createsuperuser
pytest
```