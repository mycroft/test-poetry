#!/bin/sh

set -e

cd $(git rev-parse --show-toplevel)

poetry run pytest
poetry run pylint $(git ls-files '*.py')
poetry run flake8
poetry run black -l 79 .
