#!/bin/bash

set -o errexit
set -o nounset


rm -f './celerybeat.pid'

sleep 5

celery -A src.core.celery worker -l INFO -Q beats -E -B
