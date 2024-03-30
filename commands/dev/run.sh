#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

source ./commands/dev/load-env.sh

if [ "${DEBUG}" = 1 ]; then
  echo "Starting development"
  docker-compose --profile dev start
fi