#!/bin/bash

set -o errexit
set -o nounset

sleep 5

export CELERY_BROKER_URL="redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}"

worker_ready() {
    celery -A src.core.celery inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

celery \
    -A src.core.celery  \
    -b "${CELERY_BROKER_URL}" \
    flower \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
