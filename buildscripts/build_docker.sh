#! /usr/bin/env bash
set -e

# Change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# Build the docker image
cd src || exit 1

# Build the docker image
docker build \
--tag "ai-enhanced-platform:latest" \
. || die "Failed to build"
