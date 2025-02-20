#!/bin/bash

CONTAINER_NAME="grafana-user-adder-container"

function show_help {
    echo "Usage: $0 [option]"
    echo
    echo "Options:"
    echo "  --start       Start the main loop for adding users to teams"
    echo "  --stop        Stop the running Docker container"
    echo "  --restart     Restart the Docker container"
    echo "  --teams       List all teams from Grafana"
    echo "  help          Show this help message"
    exit 0
}

case "$1" in

  --start)
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
      echo "Container is already running."
      exit 0
    fi

    # Ensure required files are present
    if [ ! -f add_users_to_team.py ]; then
        echo "Python script not found!"
        exit 1
    fi

    if [ ! -f settings.json ]; then
        echo "Settings file not found!"
        exit 1
    fi

    echo "Building the Docker image with dependencies pre-installed..."
    docker build -t grafana-user-adder . <<EOF
FROM python:3.9-slim
WORKDIR /app
COPY add_users_to_team.py settings.json /app/
RUN pip install requests
EOF

    echo "Running the Docker container..."
    docker run --rm -d \
      --name $CONTAINER_NAME \
      -v "$(pwd)":/app \
      -w /app \
      grafana-user-adder \
      python add_users_to_team.py

    if [ $? -eq 0 ]; then
      echo "Docker container started successfully."
    else
      echo "Failed to start Docker container."
    fi
    ;;

  --stop)
    echo "Stopping the running Docker container..."
    docker stop $CONTAINER_NAME
    ;;

  --restart)
    echo "Restarting the Docker container..."
    docker stop $CONTAINER_NAME && \
    docker start $CONTAINER_NAME
    ;;

  --teams)
    echo "Fetching teams from Grafana..."
    docker run --rm \
      -v "$(pwd)":/app \
      -w /app \
      grafana-user-adder \
      python add_users_to_team.py --teams
    ;;

  help)
    show_help
    ;;

  *)
    show_help
    ;;
esac