# models.py
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    category = db.Column(db.String(100))
    price = db.Column(db.Numeric(10,2))
