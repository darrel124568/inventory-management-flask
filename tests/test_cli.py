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

