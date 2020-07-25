## What is this

This demo shows how two boxes can communicate using Docker and docker-compose.

docker-compose automatically creates a network for the containers and assigns hostnames to them.

## Running

    docker-compose up --build

Then, watch the output. Notice that `web` runs an HTTP server on port 8000, and that `client` sends an HTTP request to `web`, and receives an HTTP response.