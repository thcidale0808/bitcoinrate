PIPENV=pipenv run
REVISION=head
UNAME_S := $(shell uname -s)

all: setup test

setup-python:
	CPPFLAGS="-I/usr/local/include -L/usr/local/lib" pipenv install --dev -e .

setup-deps:
ifeq ($(UNAME_S),Darwin)
	brew install snappy
else
	# If Linux assuming Ubuntu as used in CI
	apt-get update && apt-get install -y libsnappy-dev
endif

setup: setup-deps setup-python

create-revision: db require-name
	$(PIPENV) docker-compose run dbmigrations revision --autogenerate -m $(NAME)

migrate-up: db
	$(PIPENV) docker-compose run dbmigrations upgrade $(REVISION)

migrate-down: db
	$(PIPENV) docker-compose run dbmigrations downgrade $(REVISION)

#### API / DATABASE ####

db:
	docker-compose up -d db
	$(call await,docker-compose exec -T db pg_isready)

run-api: db
	docker-compose run -p 5000:5000 -d api

run-extractor: db migrate-up
	docker-compose run extractor python3 -m extractor.rate_extractor

docs-view:
	@echo Docs will be served on http://localhost:8080
	docker-compose up -d docs

#### TESTS ####

test: test-db
	$(PIPENV) bash -c 'POSTGRES_USER=$$TEST_POSTGRES_USER POSTGRES_PASSWORD=$$TEST_POSTGRES_PASSWORD \
	POSTGRES_DB=$$TEST_POSTGRES_DB POSTGRES_PORT=$$TEST_POSTGRES_PORT \
	coverage run --source=$${COVERAGE_DIRECTORIES} -m py.test tests/unit -s'
	$(PIPENV) coverage report -m
	@echo Detailed Breakdown: file://$${PWD}/htmlcov/index.html

test-db:
	docker-compose up -d unit_test_db
	$(call await,docker-compose exec -T unit_test_db pg_isready)
