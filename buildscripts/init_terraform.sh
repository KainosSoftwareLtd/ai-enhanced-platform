#! /usr/bin/env bash
set -e

# Change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# Add a command-line argument for the local flag
while getopts l: flag
do
    case "${flag}" in
        l) local=${OPTARG};;
    esac
done


# Load environment variables from .env file
export $(cat .env | xargs)

# Change to the terraform directory
cd terraform/envs/latest 

# If the local flag is set to true then check if a user is already logged in
if [ "${local}" = "true" ]; then
  # Initialise terraform locally
  terraform init
else
  # Initialise terraform in a remote backend
  terraform init -backend-config="resource_group_name=${BACKEND_RESOURCE_GROUP}" -backend-config="storage_account_name=${BACKEND_STORAGE_ACCOUNT}" -backend-config="container_name=${BACKEND_CONTAINER_NAME}" 
fi

