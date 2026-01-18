#!/bin/bash

# Navigate to sensor-node directory
cd "$(dirname "$0")/.."

PID_FILE="scripts/sensor_server.pid"

if [ -f "$PID_FILE" ]; then
    if ps -p $(cat "$PID_FILE") > /dev/null; then
        echo "Sensor server is already running (PID: $(cat "$PID_FILE"))"
        exit 1
    else
        echo "Found stale PID file. Removing..."
        rm "$PID_FILE"
    fi
fi

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start server
echo "Starting sensor server (uvicorn)..."
# redirect stdout/stderr to sensor_server.log
nohup uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}" > scripts/sensor_server.log 2>&1 &
PID=$!
echo $PID > "$PID_FILE"
echo "Sensor server started with PID $PID. Logs in scripts/sensor_server.log"
