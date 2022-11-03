SHELL := /bin/bash
MANAGE := python3 manage.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

freeze: ## Pin current dependencies
	pipenv run pip freeze > requirements.txt

merge: ## Resolve conflicts detected to merge
	$(MANAGE) makemigrations --merge


migrate: ## Make and run migrations
	$(MANAGE) makemigrations
	$(MANAGE) migrate

.PHONY: createsuperuser
createsuperuser: ## Run the Django server
	$(MANAGE) createsuperuser --email="admin@laregina.deals"

changepassword: ## Change password superuser
	$(MANAGE) changepassword admin@laregina.deals

.PHONY: test
test: ## Run test
	$(MANAGE) test src --verbosity=0 --parallel --failfast

collectstatic: ## Run collectstatic
	$(MANAGE) collectstatic --no-input

.PHONY: dumpdata
dumpdata: ## dumpdata on database
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json sites.site > data/site.json
	$(MANAGE) dumpdata --indent=4 --format=json account.emailaddress > data/email.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json accounts > data/users.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json category > data/categories.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json catalogue.product > data/products.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json catalogue.productattributevalue > data/attributes.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json catalogue.productimage > data/images.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json checkout > data/orders.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json voucher > data/vouchers.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json reviews > data/reviews.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json pages > data/pages.json


.PHONY: loaddata
loaddata: ## Load default data
	$(MANAGE) loaddata data/*.json

.PHONY: crontabadd
crontabadd: ## Add all defined jobs from CRONJOB to crontab
	$(MANAGE) crontab add

.PHONY: crontabshow
crontabshow: ## Show current active jobs of this project
	$(MANAGE) crontab show

.PHONY: gunicorn
gunicorn: ## Run project with gunicorn
	gunicorn --workers=3 --bind 127.0.0.1:9090 core.wsgi
