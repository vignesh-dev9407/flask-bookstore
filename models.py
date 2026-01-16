from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(200))
    sold = db.Column(db.Boolean, default=False)   # 👈 ADD THIS



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
