import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .app import create_app
from .database.models import setup_db, Dish, Restaurant, Category

ADMIN_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NDg2NDVjNmRiYzkwZDNkZTJkMDdjIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkxMzI3MTEzLCJleHAiOjE1OTE0MTM1MTMsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTpkaXNoZXMiLCJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6ZGlzaGVzIiwicGF0Y2g6cmVzdGF1cmFudHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRpc2hlcyIsInBvc3Q6cmVzdGF1cmFudHMiXX0.fOUB0BtNkqdtFBQXxI9tfQVKdnZNu7Fc8HHcAG64ZuDxxEb_hYtDWstyFWO3bIa-0SpjMqXZR4hoHuJKXaAsD--V4f7I-KwogXWXiqpKg-ci49lIWBiQ_4ytXjV0-tanZutWyLS9q1jg5HM5DowtFTx2adyfVy2mbjX8viggAwsNck4KIUFMr_qRHaN7okR1X3o7il2bX71zbc5khn2qruapZ_8rjcKfzHZRneWvR9zucL8slLhQNr6F5crxBP1haYjGdTODBsM-oXXGu2oUxRu82mWBTlpMa8aMs6EJPjuAr--GGtYbcwsrvJzeuEAY5ZqZI64xNFVt5tCKcPiD4Q"
USER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5NTVhN2MzNDdlYjAwYzE3MThhM2MzIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkxMzI3MTg4LCJleHAiOjE1OTE0MTM1ODgsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiXX0.KRdQcNUyH7yNOhkrjZqARrN70bVMKteQqMZwVxRnw7jHxLMImzJFvjzedAEB3koa9Nglj-nfHcuwOdUxsNYHofw61Aio9GhBj0ExT7m__1jAAz3kK-9S8n4BBA8fSdlqNnLetTHd73gKMOl0O8OFhq-sjf_I6t40yBte8nTrCE0-Oq2FEhiZb3QIWcXiw-hUo3CFU2WzUOuATQAY3GiG3DXZ7KLViX032UyqAY-2Ipbo0iM_HGbD7PetGIPmk0LQADOryZeNqDWa1xMZLyWJPcD_dDlHIv1_BRtr6JPisg5-1z_fWEcf5V5lsXfbTEuZzKbrReBW2OGAJWOCP9A-8Q"

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
    
    # ### TEST ADMIN ROLE
    # # Test admin post categories
    def test_add_categories_admin(self):
        res = self.client().post('/categories', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_add_categories_admin(self):
        category_id = 1000
        res = self.client().post('/categories' + str(category_id), json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # #Test admin get categories
    def test_get_categories_admin(self):
        res = self.client().get("/categories", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
    
    def test_404_get_categories_admin(self):
        res = self.client().get("/categories/10000", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code, 404)
    
    def test_patch_category_admin(self):
        category_id = 1
        res = self.client().patch('/categories/' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'category':'Spanish'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_403_patch_category(self):
        category_id = 1
        res = self.client().patch('/categories/' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json={'category':'Spanish'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # def test_add_restaurants_admin(self):
    #     res = self.client().post('/restaurants', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_restaurants)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_get_restaurants_admin(self):
    #     res = self.client().get("/restaurants", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['restaurants'])

    # def test_patch_restaurants_admin(self):
    #     restaurant_id = 1
    #     res = self.client().patch('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'city':'New York Patch Test'})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_add_dishes_admin(self):
    #     res = self.client().post('/dishes', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_dishes)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
    def test_get_dishes_admin(self):
        res = self.client().get("/dishes", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['dishes'])
    
    def test_404_get_dishes_admin(self):
        dish_id = 10000
        res = self.client().get("/dishes/" + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code, 404)
    
    # def test_patch_dishes_admin(self):
    #     dish_id = 5
    #     res = self.client().patch('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'rating':5})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
    #     ### TEST USER ROLE
    # # Test user post categories
    # def test_403__add_categories_user(self):
    #     res = self.client().post('/categories', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json=self.new_categories)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)


    # #Test user get categories
    # def test_get_categories_user(self):
    #     res = self.client().get("/categories", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
    #     data = json.loads(res.data)
    #     print(data)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['categories'])
    
    # def test_404_get_categories_user(self):
    #     category_id = 10000
    #     res = self.client().get("/categories/" + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
    #     data = json.loads(res.data)
    #     print(data)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertTrue(data['categories'])

    # def test_403_patch_category_user(self):
    #     category_id = 1
    #     res = self.client().patch('/categories/' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json={'category':'Spanish'})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)

    # def test_403_add_restaurants_user(self):
    #     res = self.client().post('/restaurants', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json=self.new_restaurants)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)

    def test_get_restaurants_user(self):
        res = self.client().get("/restaurants", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
    
    # def test_404_get_restaurants_user(self):
    #     res_id = 10000
    #     res = self.client().get("/restaurants/" + str(res_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertTrue(data['restaurants'])

    # def test_403_patch_restaurants_user(self):
    #     restaurant_id = 1
    #     res = self.client().patch('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json={'city':'New York Patch Test'})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)

    # def test_403_add_dishes_user(self):
    #     res = self.client().post('/dishes', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json=self.new_dishes)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)
    
    def test_get_dishes_user(self):
        res = self.client().get("/dishes", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['dishes'])
    
    def test_404_get_dishes_user(self):
        dish_id = 10000
        res = self.client().get("/dishes/" + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code, 404)
    
    # def test_403_patch_dishes_user(self):
    #     dish_id = 5
    #     res = self.client().patch('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json={'rating':5})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

        
