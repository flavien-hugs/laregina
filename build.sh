#!/usr/bin/env bash
# exit on error
set -o errexit

make deps
make collectstatic --no-input
make migrate