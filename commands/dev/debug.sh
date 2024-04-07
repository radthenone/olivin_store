#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

source ./commands/dev/load-env.sh

if [ "${DEBUG}" = 1 ]; then
  echo "Starting debugging"
  docker-compose --profile dev stop
  docker-compose --profile dev-less start
  docker-compose run --rm --service-ports backend
fi
