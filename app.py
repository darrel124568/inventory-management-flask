import flask

app = flask.Flask(__name__)

products = []
'''
Build GET, POST, PATCH, DELETE routes for /api/products.
'''

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