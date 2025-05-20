from models import db, Product
import redis
import json
import os
import redis
import json

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(redis_url, decode_responses=True)


# Cria um novo produto
def create_product(data):
    product = Product(
        description=data['description'],
        category=data['category'],
        price=data['price']
    )
    db.session.add(product)
    db.session.commit()

    # Limpa o cache após a criação
    redis_client.delete('products')
    return product

# Retorna todos os produtos, com cache Redis
def get_all_product():
    cached_products = redis_client.get('products')

    if cached_products:
        return json.loads(cached_products)

    products = Product.query.all()
    result = [{
        'id': p.id,
        'description': p.description,
        'category': p.category,
        'price': float(p.price)
    } for p in products]

    # Armazena no cache por 60 segundos
    redis_client.set('products', json.dumps(result), ex=60)
    return result

# Atualiza um produto pelo ID
def update_product(product_id, data):
    product = Product.query.get(product_id)
    if not product:
        return None

    product.description = data.get('description', product.description)
    product.category = data.get('category', product.category)
    product.price = data.get('price', product.price)
    db.session.commit()

    # Limpa cache após update
    redis_client.delete('products')
    return product

# Deleta um produto pelo ID
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return False

    db.session.delete(product)
    db.session.commit()

    # Limpa cache após delete
    redis_client.delete('products')
    return True
