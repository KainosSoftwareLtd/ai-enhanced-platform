#! /usr/bin/env bash
set -e

# Change current working directory to be the root, regardless of how this script is invoked
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

pwd

# cd into inference dir
cd inference/src || exit 1

pwd

# Build the docker image

docker build \
--tag "aep-inference:latest" \
. || die "Failed to build"  
  