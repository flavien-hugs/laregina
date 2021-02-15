#!/usr/bin/env bash

set -o errexit

make deps
make collectstatic --no-input
make migratedb