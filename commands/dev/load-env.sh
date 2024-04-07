#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "Loading development environment"
source "${PWD}"/.envs/dev/react.env
source "${PWD}"/.envs/dev/django.env
source "${PWD}"/.envs/dev/postgres.env
source "${PWD}"/.envs/dev/redis.env
