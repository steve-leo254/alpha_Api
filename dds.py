from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app=Flask(__name__)
app.secret_key='secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:leo.steve@localhost/alpha-products'
db = SQLAlchemy(app)




class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float,nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)