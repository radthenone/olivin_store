#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

delete_migrations() {
    local directory="$1"
    if [ -d "$directory" ]; then
        echo "Deleting files in directory: $directory"
        find "$directory" -type f ! -name '__init__.py' -delete
    fi
}

find "$PWD" -type d -name 'migrations' | while read -r migrations_dir; do
    delete_migrations "$migrations_dir"
done
