#! /usr/bin/env bash

set -e

cd "$(dirname "${BASH_SOURCE[0]}")/../docs/mkdocs"

docker build --tag "aep-mkdocs:latest" . || die "Failed to build"

