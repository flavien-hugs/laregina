SHELL := /bin/bash
MANAGE := ./manage.py

TEST_SETTINGS := test

.PHONY: all help deps static migrate restart update deploy

all: help

help:
	@echo "Usage:"
	@echo "  make deploy - pull and deploy the update"
	@echo "  make test - run automated tests"

deps:
	pipenv install

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

dumpdata:
	$(MANAGE) dumpdata --indent=4 accounts.user > fixtures/users_data.json
	$(MANAGE) dumpdata --indent=4 category.category > fixtures/category_data.json
	$(MANAGE) dumpdata --indent=4 catalogue.product > fixtures/product_data.json

loaddata:
	$(MANAGE) loaddata fixtures/users_data.json
	$(MANAGE) loaddata fixtures/category_data.json
	$(MANAGE) loaddata fixtures/product_data.json

test:
	$(MANAGE) test $(TEST_SETTINGS)
