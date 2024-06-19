#! /usr/bin/env bash
set -e

# Change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# Go to terraform directory
cd terraform/envs/stable 

# Destroy terraform
terraform destroy -auto-approve -var="system_api_key=${SYSTEM_API_KEY}" -var="docker_registry_password=${DOCKER_REGISTRY_PASSWORD}" -var="docker_registry_username=${DOCKER_REGISTRY_USERNAME}"