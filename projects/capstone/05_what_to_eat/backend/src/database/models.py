import os
from sqlalchemy import Column, String, Integer, Numeric
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

# database_name = "dish"
project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
default_dish_image_link = "https://unsplash.com/photos/1Rm9GLHV0UA"
default_restaurant_image_link = "https://unsplash.com/photos/26T6EAsQCiA"
db = SQLAlchemy()

'''
setup_db(app) binds a flask application and a SQLAlchemy service.
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


'''
Dish Model
'''


class Dish(db.Model):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    restaurant_id = Column(
        Integer, db.ForeignKey('restaurants.id'), nullable=False)
    category_id = Column(
        Integer, db.ForeignKey('categories.id'), nullable=False)
    rating = Column(Integer)
    price = Column(Numeric(10, 2))
    image_link = Column(String(500))

    def __init__(
            self, name, restaurant_id, category_id, rating, price, image_link):
        self.name = name
        self.restaurant_id = restaurant_id
        self.category_id = category_id
        self.rating = rating
        self.price = price
        self.image_link = image_link

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
            'category_id': self.category_id,
            'rating': self.rating,
            'price': float(self.price),
            'image_link': self.image_link or default_dish_image_link
        }


'''
Category Model
'''


class Category(db.Model):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)
    dishes = db.relationship("Dish", backref=db.backref('category', lazy=True))

    def __init__(self, category):
        self.category = category

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
            "id": self.id,
            "category": self.category
        }


'''
Restaurant Model
'''


class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    address = Column(String(180), nullable=False)
    website = Column(String(120), nullable=False)
    r_image_link = Column(String(500))
    dishes = db.relationship("Dish", backref=db.backref(
        'restaurant', lazy=True))

    def __init__(self, name, city, state, address, website, r_image_link):
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.website = website
        self.r_image_link = r_image_link

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
            'address': self.address,
            'website': self.website,
            'r_image_link': self.r_image_link or default_restaurant_image_link
        }
