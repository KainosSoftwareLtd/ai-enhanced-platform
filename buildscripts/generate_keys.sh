#! /usr/bin/env bash
set -e

# Change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# Install pip requirements
cd keymanagement && pip install -r requirements.txt

# Create keys
python3 key_gen.py