#!/bin/bash

wait_for_port() {
    local host=$1
    local port=$2
    local timeout=${3:-30}
    # shellcheck disable=SC2155
    local start_time=$(date +%s)

    while true; do
        if nc -z -w 1 "$host" "$port" >/dev/null 2>&1; then
            echo "Port $port is open on $host"
            return 0
        else
            local elapsed_time=$(($(date +%s) - "$start_time"))
            if [ "$elapsed_time" -ge "$timeout" ]; then
                echo "Timeout waiting for $host:$port"
                return 1
            fi
            sleep 1
        fi
    done
}

if [ $# -ne 2 ]; then
    echo "Usage: $0 <host> <port>"
    exit 1
fi

host=$1
port=$2

if wait_for_port "$host" "$port"; then
    echo "Continuing with the script..."
else
    echo "Exiting the script."
    exit 1
fi
