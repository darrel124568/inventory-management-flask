import flask
import requests

app = flask.Flask(__name__)

products = []
'''
Build proxy routes to OpenFoodFacts via Python requests
'''

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }
    
@app.route('/')
def index():
    redirect_url = flask.url_for('get_products')
    return flask.redirect(redirect_url)
    
@app.route('/api/products/<barcode>', methods=['GET'])
def get_product(barcode):
    product_data = get_product_by_barcode(barcode)
    if product_data:
        return flask.jsonify(product_data["product"]["_keywords"])
    else:
        return flask.jsonify({'error': 'Product not found'}), 404

@app.route('/api/products', methods=['GET'])
def get_products():
    return flask.jsonify([product.to_dict() for product in products])

@app.route('/api/products', methods=['POST'])
def create_product():
    data = flask.request.get_json()
    product_id = len(products) + 1
    product = Product(id=product_id, name=data['name'], price=data['price'])
    products.append(product)
    return flask.jsonify(product), 201

@app.route('/api/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        return flask.jsonify({'error': 'Product not found'}), 404
    data = flask.request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    return flask.jsonify(product)

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p.id != product_id]
    return flask.jsonify({'message': 'Product deleted'}), 200

if __name__ == "__main__":
    app.run(debug=True)