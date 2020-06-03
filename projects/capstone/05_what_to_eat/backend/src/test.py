import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from .database.models import setup_db, Dish, Restaurant, Category

class WhatToEatTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "dishes_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_dishes = {
            "category": "Asian",
            "category_id": 2,
            "id": 4,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "Star bird Sandwich",
            "price": 15,
            "rating": 5,
            "restaurant_id": 1,
            "restaurant_name": "Star bird"
        }
        
        self.new_categories = {
            "category": "Mexican"
        }

        self.new_restaurants = {
            "city": "San Francisco",
            "name": "Roy restaurant",
            "address": "Test address",
            "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
            "state": "CA",
            "website": "www.royrestaurant.com"
        }
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.load(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

        
