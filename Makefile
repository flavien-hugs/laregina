SHELL := /bin/bash
MANAGE := python manage.py

TEST_SETTINGS := test

.PHONY: all help deps static migrate restart update deploy

all: help

help:
	@echo "Usage:"
	@echo "  make deploy - pull and deploy the update"
	@echo "  make test - run automated tests"

install-deps:
	pip install -r requirements.txt

deps:
	pipenv install

runserver:
	$(MANAGE) runserver

migratedb:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

dumpdata:
	$(MANAGE) dumpdata --format=json accounts.user > __backups__/users_data.json
	$(MANAGE) dumpdata --format=json category.category > __backups__/category_data.json

loaddata:
	$(MANAGE) loaddata __backups__/users_data.json
	$(MANAGE) loaddata __backups__/category_data.json

test-deploy:
	$(MANAGE) test check --deploy

install-project:
	pip install -r requirements.txt
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) loaddata __backups__/users_data.json