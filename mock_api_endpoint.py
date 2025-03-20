from faker import Faker
from flask import Flask, jsonify

fake = Faker('en_US')
app = Flask(__name__)


@app.route('/api/products')
def get_products():
    """API endpoint which returns 10 fake products"""
    products = [
        {
            "product_id": fake.uuid4(),
            "name": fake.word().capitalize() + " " + fake.word().capitalize(),
            "description": fake.sentence(),
            "price": fake.random_int(min=100, max=5000),
            "image_url": fake.image_url()  # Fake image URL
        } for _ in range(10)  # Generate 10 products
    ]
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)