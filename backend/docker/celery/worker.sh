#!/bin/bash

set -o errexit
set -o nounset

sleep 5

celery -A src.core.celery worker --loglevel=info
