import os
import sys
import pytest
import requests
from server import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#tests if fetching of a barcode works correctly and handles edge cases like invalid barcodes or network issues.
#product is validated once the fetch is successful by checking expected values
def test_get_product_by_barcode_valid():
    barcode = "5449000000996"  #valid barcode 
    product_data = app.get_product_by_barcode(barcode)
    assert product_data is not None
    assert "product" in product_data
    assert product_data["product"]["code"] == barcode

#tests edge case of an invalid barcode, expecting the function to return None and handle the error gracefully.
def test_get_product_by_barcode_invalid():
    barcode = "invalid_code"  # Invalid barcode
    product_data = app.get_product_by_barcode(barcode)
    assert product_data is None

#test network issues by mocking the requests.get method to raise a RequestException, ensuring that the function returns None and handles the exception without crashing.
def test_network_issue(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Network error")
    
    monkeypatch.setattr(requests, "get", mock_get)
    
    barcode = "5449000000996"
    product_data = app.get_product_by_barcode(barcode)
    assert product_data is None


#testing Create operations
@pytest.fixture
def client():
    return app.app.test_client()

def test_create_product(client):
    # Test creating a product with a valid barcode
    response = client.post('/api/products', json={"barcode": "5449000000996"})
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data
    assert "name" in data
    assert "price" in data

    # Test creating a product with an invalid barcode
    response = client.post('/api/products', json={"barcode": "invalid_code"})
    assert response.status_code == 404

#testing Read operations
def test_get_products(client):
    # Test getting the list of products
    response = client.post('/api/products', json={"barcode": "5449000000996"})
    # Test getting the list of products
    response = client.get('/api/products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Test that the list contains at least one product
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]

#testing Update operations
def test_update_product(client):
    # Create a product to update
    response = client.post('/api/products', json={"barcode": "5449000000996"})
    product_id = response.get_json()["id"]

    # Test updating the product's name and price
    response = client.patch(f'/api/products/{product_id}', json={"name": "New name", "price": 19.99})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "New name"
    assert data["price"] == 19.99

    # Test updating a non-existent product
    response = client.patch('/api/products/9999', json={"name": "Non-existent Product"})
    assert response.status_code == 404