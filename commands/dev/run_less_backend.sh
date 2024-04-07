#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

source ./commands/dev/load-env.sh

if [ "${DEBUG}" = 1 ]; then
  echo "Starting development wait for backend"
  docker-compose --profile less-dev start
fi
