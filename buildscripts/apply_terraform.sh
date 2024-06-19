#! /usr/bin/env bash
set -e

# Change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# Change to the terraform directory
cd terraform/envs/latest 

# Apply terraform
terraform apply -auto-approve out.tfplan