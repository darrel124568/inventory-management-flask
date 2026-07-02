import flask

app = flask.Flask(__name__)

products = []
'''
Build GET, POST, PATCH, DELETE routes for /api/products.
'''
@app.route('/api/products', methods=['GET'])
def get_products():
    return flask.jsonify(products)

@app.route('/api/products', methods=['POST'])
def create_product():
    data = flask.request.get_json()
    product_id = len(products) + 1
    product = {
        'id': product_id,
        'name': data['name'],
        'price': data['price']
    }
    products.append(product)
    return flask.jsonify(product), 201

@app.route('/api/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return flask.jsonify({'error': 'Product not found'}), 404
    data = flask.request.get_json()
    product.update(data)
    return flask.jsonify(product)

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return flask.jsonify({'message': 'Product deleted'}), 200

if __name__ == "__main__":
    app.run(debug=True)