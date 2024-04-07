#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

source ./commands/dev/load-env.sh

if [ "${DEBUG}" = 1 ]; then
  echo "Starting install development"
  docker-compose --profile dev up --build -d
  docker-compose --profile dev stop
  echo "Development created"
fi
