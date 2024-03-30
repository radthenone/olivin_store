#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

if [ "$#" -gt 1 ]; then
  echo "Usage: $0 [--delete]" >&2
  exit 1
fi

if [ "$#" -eq 1 ] && [ "$1" != "--delete" ]; then
  echo "Usage: $0 [--delete]" >&2
  exit 1
fi

DELETE="${1:-}"

if [ "$DELETE" = "--delete" ]; then
  docker-compose --profile backend stop db
  docker-compose --profile backend down -v db
  docker-compose --profile backend up --build -d db
  source ./commands/dev/backend/delete_migrations_files.sh
  source ./commands/dev/load-env.sh
  docker-compose --profile backend run --rm backend sh -c "python manage.py makemigrations"
  docker-compose --profile backend run --rm backend sh -c "python manage.py migrate"
  docker-compose --profile backend run --rm backend sh -c "python -m src.users.commands.create_superuser --email '${DJANGO_SUPERUSER_EMAIL}' --password '${DJANGO_SUPERUSER_PASSWORD}'"
else
  docker-compose --profile backend run --rm backend sh -c "python manage.py makemigrations"
  docker-compose --profile backend run --rm backend sh -c "python manage.py migrate"
fi

echo "Migrations created"
