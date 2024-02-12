from datetime import datetime
from main  import db 

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)