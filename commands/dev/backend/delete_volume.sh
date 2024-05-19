#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

if [ $# -ne 2 ]; then
    echo "Need to specify the container and volume names."
    echo "delete_volume.sh <container_name> <volume_name>"
    exit 1
fi

container_name=$1
volume_name=$2

docker container rm -f "$container_name"
docker volume rm "$volume_name"
