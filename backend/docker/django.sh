#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

sleep 2

echo "========== DJANGO MIGRATIONS =========="
python manage.py migrate

echo "========== DJANGO SUPERUSER =========="
admin_exists() {
    python <<END
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings.base')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(is_superuser=True).exists():
    print("True")
else:
    print("False")
END
}

if [[ $(admin_exists) == "False" ]]; then
    echo "Admin user does not exist. Creating..."
    export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}"
    export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}"
    export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}"
    python manage.py createsuperuser \
        --email "${DJANGO_SUPERUSER_EMAIL}" \
        --noinput
else
    echo "Admin user exists. No action required."
fi

echo "Continuing with the execution."

echo "========== DJANGO RUNSERVER =========="

uvicorn src.core.asgi:application --host "${DJANGO_HOST}" --port "${DJANGO_PORT}" --reload --lifespan "off"

exec "$@"