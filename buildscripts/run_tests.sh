#! /usr/bin/env bash
set -e

# change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# run the test suite with coverage
cd src || exit 1

coverage run -m pytest tests/