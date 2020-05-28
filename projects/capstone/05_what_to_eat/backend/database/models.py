import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "dish"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgresql://{}/{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Dish(db.Model):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    restaurant_id = Column(Integer)
    category = Column(String)
    rating = Column(Integer)

    def __init__(self, name, restaurant_id, category, rating):
        self.name = name
        self.restaurant_id = restaurant_id
        self.category = category
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'restaurant_id': self.restaurant_id,
            'category': self.category,
            'rating': self.rating
        }


class Category(db.Model):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category = Column(String)

    def __init__(self, category):
        self.category = category
    
    def format(self):
        return {
            "id": self.id,
            "category": self.category
        }

class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    address = Column(String)
    website = Column(String)

    def __init__(self, name, city, state, website):
        self.name = name
        self.city = city
        self.state = state
        self.website = website

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'website': self.website
        }