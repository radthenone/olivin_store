#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE}"

echo "Continuing with the execution."

echo "========== DJANGO RUNSERVER =========="

python app.py --wsgi

exec "$@"
