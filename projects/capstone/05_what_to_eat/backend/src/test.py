import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .app import create_app
from .database.models import setup_db, Dish, Restaurant, Category

ADMIN_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NDg2NDVjNmRiYzkwZDNkZTJkMDdjIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkxMjQ0NzIxLCJleHAiOjE1OTEzMzExMjEsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTpkaXNoZXMiLCJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6ZGlzaGVzIiwicGF0Y2g6cmVzdGF1cmFudHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRpc2hlcyIsInBvc3Q6cmVzdGF1cmFudHMiXX0.ZdnwPVNv5wR1YBfBc0q9BOytF-Jw8rPfjg0_4nmyUbSPh_WZa5fWQ9MaQH9ofyljtq9IdAzdo7A7UqKylT04Go9ySIV1Z6ekvOqZmO0aYIK4nwxeUPcjjCTrRyZU1uZ8USYI4UPqvR233Mg19G-hx2GoB9YrGK-wq69W73LpH1cahLwRoZdmL89Qii6GPd60Ei8sfnIBsUaLYQu3iw8DSKT80Rj5YhbU2ljeme42ZRTAjKd4NmngyPxdesKde3cBmHrtzvbQuD295-tR_Y2INdGLCuaJs51DlIaBG6LuEb5XsJ7PwTkO32VzPg2efQ23tg4l2HonBTgez-lDaDjWvQ"
#USER_TOKEN =

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

        # self.admin_headers = {
        #     "Content-Type": "application/json",
        #     "Bearer {}".format(ADMIN_TOKEN)
        # }
        
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    ### TEST ADMIN ROLE
    # Test admin post categories
    def test_add_categories_admin(self):
        res = self.client().post('/categories', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_add_categories_admin(self):
        category_id = 1000
        res = self.client().post('/categories' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    #Test admin get categories
    def test_get_categories_admin(self):
        res = self.client().get("/categories", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    # def test_patch_category_admin(self):
    #     category_id = 1
    #     res = self.client().patch('/categories/1' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'category':'Spanish'})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
    def test_401_get_categories_admin(self):
        res = self.client().get("/categories", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format('')})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
    
    def test_add_restaurants_admin(self):
        res = self.client().post('/restaurants', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_restaurants)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_restaurants_admin(self):
        res = self.client().get("/restaurants", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['restaurants'])

    def test_patch_restaurants_admin(self):
        restaurant_id = 1
        res = self.client().patch('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'city':'New York Patch Test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_dishes_admin(self):
        res = self.client().post('/dishes', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_dishes)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_dishes_admin(self):
        res = self.client().get("/dishes", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['dishes'])
    
    def test_patch_dishes_admin(self):
        dish_id = 5
        res = self.client().patch('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'rating':5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

        
