import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import cli

# A mock response class to simulate requests responses
class MockResponse:
    def __init__(self, status_code, json_data=None, text=''):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text

    def json(self):
        return self._json_data

# Test cases for the CLI
def test_cli_add_product_success(monkeypatch, capsys):
    def mock_post(url, json):
        return MockResponse(200, {"id": 1, "name": "Test Product", "price": 10.0})

    monkeypatch.setattr(cli.requests, "post", mock_post)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--add", "5449000000996"])

    cli.main()

    captured = capsys.readouterr()
    assert "Product added successfully!" in captured.out
    assert "Test Product" in captured.out


def test_cli_add_product_failure(monkeypatch, capsys):
    def mock_post(url, json):
        return MockResponse(404, {"error": "Product not found"}, text='Product not found')

    monkeypatch.setattr(cli.requests, "post", mock_post)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--add", "12345"])

    cli.main()

    captured = capsys.readouterr()
    assert "Failed to add product" in captured.out
    assert "404" in captured.out

#Test adding an already existing product, expecting the quantity to increment instead of creating a new product
def test_cli_add_existing_product(monkeypatch, capsys):
    def mock_post(url, json):
        return MockResponse(200, {"id": 1, "name": "Test Product", "price": 10.0, "quantity": 2})

    monkeypatch.setattr(cli.requests, "post", mock_post)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--add", "5449000000996"])

    cli.main()

    captured = capsys.readouterr()
    assert "Product added successfully!" in captured.out
    assert "Test Product" in captured.out
    assert "'quantity': 2" in captured.out

#Remove product successfully
def test_cli_remove_product_success(monkeypatch, capsys):
    def mock_delete(url):
        return MockResponse(200)

    monkeypatch.setattr(cli.requests, "delete", mock_delete)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--remove", "1"])

    cli.main()

    captured = capsys.readouterr()
    assert "Product removed successfully!" in captured.out

#fail to remove product
def test_cli_remove_product_failure(monkeypatch, capsys):
    def mock_delete(url):
        return MockResponse(404, {"error": "Product not found"}, text='Product not found')

    monkeypatch.setattr(cli.requests, "delete", mock_delete)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--remove", "999"])

    cli.main()

    captured = capsys.readouterr()
    assert "Failed to remove product" in captured.out
    assert "404" in captured.out


#Test listing products successfully
def test_cli_list_products(monkeypatch, capsys):
    products = [
        {"id": 1, "name": "Test Product", "price": 10.0},
        {"id": 2, "name": "Another Product", "price": 20.0},
    ]

    def mock_get(url):
        return MockResponse(200, products)

    monkeypatch.setattr(cli.requests, "get", mock_get)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--list"])

    cli.main()

    captured = capsys.readouterr()
    assert "Current Inventory:" in captured.out
    assert "Another Product" in captured.out


#Test listing products when no products are found
def test_cli_list_no_products(monkeypatch, capsys):
    def mock_get(url):
        return MockResponse(200, [])

    monkeypatch.setattr(cli.requests, "get", mock_get)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--list"])

    cli.main()

    captured = capsys.readouterr()
    assert "No products found in inventory." in captured.out

#test updating product successfully
def test_cli_update_product_success(monkeypatch, capsys):
    def mock_patch(url, json):
        return MockResponse(200, {"id": 1, "name": json.get('name', 'Existing'), "price": json.get('price', 10.0)})

    monkeypatch.setattr(cli.requests, "patch", mock_patch)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--update", "1"])
    monkeypatch.setattr('builtins.input', lambda prompt='': 'New Name' if 'name' in prompt.lower() else '15.99')

    cli.main()

    captured = capsys.readouterr()
    assert "Product updated successfully!" in captured.out
    assert "New Name" in captured.out

#Test updating product failure
def test_cli_update_product_failure(monkeypatch, capsys):
    def mock_patch(url, json):
        return MockResponse(404, {"error": "Product not found"}, text='Product not found')

    monkeypatch.setattr(cli.requests, "patch", mock_patch)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--update", "999"])
    monkeypatch.setattr('builtins.input', lambda prompt='': 'New Name' if 'name' in prompt.lower() else '15.99')

    cli.main()

    captured = capsys.readouterr()
    assert "Failed to update product" in captured.out
    assert "404" in captured.out

#Test getting product details successfully
def test_cli_get_product_success(monkeypatch, capsys):
    product = {"id": 1, "name": "Test Product", "price": 10.0, "barcode": "1234567890123", "quantity": 5}

    def mock_get(url):
        return MockResponse(200, product)

    monkeypatch.setattr(cli.requests, "get", mock_get)
    monkeypatch.setattr(sys, "argv", ["cli.py", "--get", "1"])

    cli.main()

    captured = capsys.readouterr()
    assert "Product Details:" in captured.out
    assert "Test Product" in captured.out