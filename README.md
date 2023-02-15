# Playwright + Django tests

Sample repository for testing the usage of Playwright in a Django project.


## Setup

```sh
poetry env use 3.11
poetry install
```

## Loading fixtures

```sh
poetry run \
    python manage.py loaddata ingredients pizzas
```

## Exporting fixtures

```sh
poetry run \
    python manage.py dumpdata pizza.Ingredient \
        -o pizza/fixtures/ingredients.json.gz
poetry run \
    python manage.py dumpdata pizza.Pizza \
        -o pizza/fixtures/pizzas.json.gz
```

## Running Django instance

```sh
poetry run \
    python manage.py runserver
```

## Running tests

```sh
poetry run \
    python manage.py test
```

## Running tests

```sh
poetry run \
    python manage.py test
```

## Generating test code with Playwright

Launch a local Django instance, then from another shell run

```sh
playwright codegen http://localhost:8000/admin
```
