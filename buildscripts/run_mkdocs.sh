#! /usr/bin/env bash
set -e

cd "$(dirname "${BASH_SOURCE[0]}")/../docs/mkdocs" || exit 1

docker stop aep-mkdocs || true && docker rm aep-mkdocs || true

docker run --name aep-mkdocs --rm -p 8000:8000 aep-mkdocs