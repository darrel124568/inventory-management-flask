# Inventory Management Flask

A simple Flask-based inventory management application with a CLI client.

## Requirements

- Python 3.12
- `pipenv` (recommended) or `venv`

## Installation

Using `pipenv`:

```bash
pip install pipenv
pipenv install
```
## Running the server

Start the Flask API server from the project root:

```bash
pipenv run python server/app.py
```

The API will run by default on `http://127.0.0.1:5000`.

## Using the CLI

From the project root, run the CLI client with one of the supported flags.

Add a product by barcode:

```bash
pipenv run python client/cli.py --add 5449000000996
```

Remove a product by ID:

```bash
pipenv run python client/cli.py --remove 1
```

List inventory items:

```bash
pipenv run python client/cli.py --list
```

Update a product by ID:

```bash
pipenv run python client/cli.py --update 1
```

Get product details by ID:

```bash
pipenv run python client/cli.py --get 1
```

## Running tests

Execute the test suite with `pytest`:

```bash
pipenv run pytest
```


## Notes

- The CLI uses the local Flask API at `http://127.0.0.1:5000/api/products`.
- The server fetches product data from OpenFoodFacts by barcode.
