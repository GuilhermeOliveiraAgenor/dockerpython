import os
from flask import Flask, request, jsonify
from config import Config
from models import db, Product
import crud

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    product = crud.create_product(data)
    return jsonify({
        'id': product.id,
        'description': product.description,
        'category': product.category,
        'price': float(product.price)
    })

@app.route('/product', methods=['GET'])
def get_product():
    # produtos já são dicionários, não objetos Product
    products = crud.get_all_product()
    return jsonify(products)

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product_route(product_id):
    data = request.get_json()
    product = crud.update_product(product_id, data)
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    return jsonify({
        'id': product.id,
        'description': product.description,
        'category': product.category,
        'price': float(product.price)
    })

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    success = crud.delete_product(product_id)
    if not success:
        return jsonify({'error': 'Produto não encontrado'}), 404
    return jsonify({'message': 'Produto deletado com sucesso'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
