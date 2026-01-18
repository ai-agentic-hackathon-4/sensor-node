#!/bin/bash

# Navigate to sensor-node directory
cd "$(dirname "$0")/.."

PID_FILE="scripts/sensor_server.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "No PID file found. Is the server running?"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null; then
    echo "Stopping sensor server (PID: $PID)..."
    kill $PID
    # Wait for process to exit
    sleep 2
    if ps -p $PID > /dev/null; then
         echo "Process did not exit, sending SIGKILL..."
         kill -9 $PID
    fi
    echo "Stopped."
else
    echo "Process $PID not running."
fi

rm "$PID_FILE"
