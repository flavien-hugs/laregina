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
	pipenv lock -r > requirements.txt

migrate: ## Make and run migrations
	$(MANAGE) makemigrations
	$(MANAGE) migrate

.PHONY: test
test: ## Run test
	$(MANAGE) test src --verbosity=0 --parallel --failfast

collectstatic: ## Run collectstatic
	$(MANAGE) collectstatic --no-input

.PHONY: dumpdata
dumpdata: ## dumpdata on database
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json accounts.user > data/user_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json accounts.profilesocialmedia > data/social_media_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json category.category > data/category_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json catalogue.product > data/product_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json catalogue.productimage > data/product_image_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json analytics.productview > data/analytics_data.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json cart.cartitem > data/cart_data.json

.PHONY: loaddata
loaddata: ## Load default data
	$(MANAGE) loaddata data/*.json
