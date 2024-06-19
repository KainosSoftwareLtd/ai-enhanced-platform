#! /usr/bin/env bash
set -e

# Change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1


# Stop any current running and remove existing containers
docker compose -f ./docker/docker-compose-inf.yml down --volumes --remove-orphans

# Run the app
docker compose -f ./docker/docker-compose-inf.yml up
