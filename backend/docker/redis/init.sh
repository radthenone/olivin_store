#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

echo "Starting redis server..."
# Start redis server
redis-server --bind 0.0.0.0 --requirepass "${REDIS_PASSWORD}" --maxmemory 256mb --maxmemory-policy allkeys-lru --appendonly yes

echo "Redis server started"