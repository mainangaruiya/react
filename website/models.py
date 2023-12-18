# models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    notes = db.relationship('Note')

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kitchen_image = db.Column(db.String(255))
    sitting_room_image = db.Column(db.String(255))
    living_room_image = db.Column(db.String(255))
    master_bedroom_image = db.Column(db.String(255))
    additional_images = db.Column(db.String(1000))
    property_title = db.Column(db.String(255))
    num_bedrooms = db.Column(db.Integer)
    property_location = db.Column(db.String(255))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('properties', lazy=True))

    def __repr__(self):
        return f"Property('{self.property_title}', '{self.property_location}', '{self.price}')"