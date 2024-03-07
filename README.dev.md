### install backend
```bash
cd backend
poetry lock --no-update
poetry install
```

### run app
```bash
cd backend
poetry run python main.py 
```

### install docker project
```bash
docker-compose -f docker-compose.dev.yml up --build -d
```

### run docker ninja-django
```bash
docker-compose -f docker-compose.dev.yml run --rm web
```

### run migrations
```bash
cd backend
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```