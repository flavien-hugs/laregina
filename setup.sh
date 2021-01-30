#!/usr/bin/env bash

pipenv install
pipenv shell
make migrate
make runserver