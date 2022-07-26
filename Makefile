SHELL := /bin/bash
MANAGE := python manage.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: pip
pip: ## Make venv and install requrements
	python3 -m pip3 install --upgrade pip3
	pip3 install --upgrade -r requirements.txt

.PHONY: venv
venv: ## Make a new virtual environment
	pip3 install pipenv
	pipenv shell

.PHONY: install
install: venv ## Install or update dependencies
	pipenv sync

freeze: ## Pin current dependencies
	pipenv run pip freeze --local > requirements.txt

migrate: ## Make and run migrations
	$(MANAGE) makemigrations
	$(MANAGE) migrate

.PHONY: createsuperuser
createsuperuser: ## Run the Django server
	$(MANAGE) createsuperuser --email="unsta.inc@pm.me"

changepassword: ## Change password superuser
	$(MANAGE) changepassword flavienhugs@gmail.com

.PHONY: test
test: ## Run test
	$(MANAGE) test src --verbosity=0 --parallel --failfast

collectstatic: ## Run collectstatic
	$(MANAGE) collectstatic --no-input

.PHONY: dumpdata
dumpdata: ## dumpdata on database
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json accounts.user > data/users_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json category.category > data/categories_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json catalogue.product > data/products_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json catalogue.productimage > data/products_image_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json checkout.order > data/orders_data.json

.PHONY: loaddata
loaddata: ## Load default data
	$(MANAGE) loaddata data/*.json

.PHONY: crontabadd
crontabadd: ## Add all defined jobs from CRONJOB to crontab
	$(MANAGE) crontab add

.PHONY: crontabshow
crontabshow: ## Show current active jobs of this project
	$(MANAGE) crontab show
