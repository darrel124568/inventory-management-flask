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
    assert "ID: 1" in captured.out
    assert "Another Product" in captured.out


