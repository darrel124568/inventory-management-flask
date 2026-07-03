import flask
import requests
import random, math

app = flask.Flask(__name__)

products = []
def get_product_by_barcode(barcode):
    try:
        response = requests.get(f"https://world.openfoodfacts.net/api/v3.6/product/{barcode}.json")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return None
        
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
        self.barcode = None  
        self.quantity = 1  

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'barcode': self.barcode,
            'quantity': self.quantity
        }

@app.route('/api/products', methods=['GET'])
def get_products():
    return flask.jsonify([product.to_dict() for product in products])

@app.route('/api/products/low-stock', methods=['GET'])
def get_low_stock_products():
    threshold = flask.request.args.get('threshold', default=2, type=int)
    low_stock = [product.to_dict() for product in products if product.quantity <= threshold]
    return flask.jsonify(low_stock)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product:
        return flask.jsonify(product.to_dict())
    else:
        return flask.jsonify({'error': 'Product not found'}), 404

@app.route('/api/products', methods=['POST'])
def create_product():
    data = flask.request.get_json()
    product_data = get_product_by_barcode(data.get('barcode'))
    if product_data:
        product_name = product_data["product"].get("product_name", "Unknown")
        existing_product = next((p for p in products if p.name == product_name), None)
        if existing_product:
            existing_product.quantity += 1
            return flask.jsonify(existing_product.to_dict())

        new_product = Product(
            id=len(products) + 1,
            name=product_name,
            price=math.floor(random.uniform(1.0, 100.0))
        )
        new_product.barcode = data.get('barcode')
        products.append(new_product)
        return flask.jsonify(new_product.to_dict())
    else:
        return flask.jsonify({'error': 'Product not found'}), 404

@app.route('/api/products/<int:product_id>', methods=['PATCH', 'PUT'])
def update_product(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        return flask.jsonify({'error': 'Product not found'}), 404
    data = flask.request.get_json()
    for key, value in data.items():
        setattr(product, key, value)
    return flask.jsonify(product.to_dict())

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        return flask.jsonify({'error': 'Product not found'}), 404
    products = [p for p in products if p.id != product_id]
    return flask.jsonify({'message': 'Product deleted'}), 200

if __name__ == "__main__":
    app.run(debug=True)