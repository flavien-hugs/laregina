#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install
./manage.py collectstatic --no-input
./manage.py makemigrations
./manage.py migrate