#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Usage: $0 --app APP_NAME [--delete]"
  exit 1
fi

if [ "$1" != "--app" ]; then
  echo "Usage: $0 --app APP_NAME [--delete]"
  exit 1
fi

APP_NAME=$2
DELETE=${3:-}

if [ -n "$DELETE" ] && [ "$DELETE" = "--delete" ]; then
  docker-compose --profile backend stop db
  docker-compose --profile backend down -v db
  docker-compose --profile backend up --build -d db
  source ./commands/dev/backend/delete_migrations_files.sh
fi

if [ -n "$APP_NAME" ]; then
  docker-compose --profile backend run --rm backend sh -c "python manage.py makemigrations $APP_NAME"
  docker-compose --profile backend run --rm backend sh -c "python manage.py migrate $APP_NAME"
else
  echo "APP_NAME is required."
fi