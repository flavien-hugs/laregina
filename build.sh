#!/usr/bin/env bash
# exit on error
set -o errexit

make deps
python manage.py collectstatic --no-input
make migrate