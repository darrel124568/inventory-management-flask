import os
import sys
import pytest
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