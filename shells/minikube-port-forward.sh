#!/bin/bash

SERVICE_NAME="postgres-service"
LOCAL_PORT=5432
REMOTE_PORT=5432

start_port_forward() {
  echo "Starting port-forwarding for service $SERVICE_NAME on port $LOCAL_PORT..."
  
  # Run port-forward in the background and save its process ID
  minikube kubectl -- port-forward svc/$SERVICE_NAME $LOCAL_PORT:$REMOTE_PORT &
  PORT_FORWARD_PID=$!

  # Save the process ID to a file for later stopping
  echo $PORT_FORWARD_PID > port_forward.pid
  echo "Port-forwarding started with PID $PORT_FORWARD_PID."
}

stop_port_forward() {
  if [ -f port_forward.pid ]; then
    PORT_FORWARD_PID=$(cat port_forward.pid)
    echo "Stopping port-forwarding with PID $PORT_FORWARD_PID..."
    kill $PORT_FORWARD_PID
    rm port_forward.pid
    echo "Port-forwarding stopped."
  else
    echo "No port-forwarding process found."
  fi
}

case "$1" in
  start)
    start_port_forward
    ;;
  stop)
    stop_port_forward
    ;;
  restart)
    stop_port_forward
    start_port_forward
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
esac
