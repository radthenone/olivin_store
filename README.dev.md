## Develop readme to use:


### install docker project
```bash
docker-compose --profile dev up --build -d
```

### run docker ninja-django
```bash
docker-compose --profile dev up -d
```

### dev project start
```bash
python manage.py runserver "0.0.0.0:8000"
```

### add migrations
```bash
./commands/dev/backend/makemigrations.sh
```

### delete all migrations
```bash
./commands/dev/backend/delete_migrations.sh
```
