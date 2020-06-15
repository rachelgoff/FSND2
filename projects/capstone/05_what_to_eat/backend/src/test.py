import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .app import create_app
from .database.models import setup_db, Dish, Restaurant, Category

ADMIN_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NDg2NDVjNmRiYzkwZDNkZTJkMDdjIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkxNDEzOTM4LCJleHAiOjE1OTE1MDAzMzgsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTpkaXNoZXMiLCJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6ZGlzaGVzIiwicGF0Y2g6cmVzdGF1cmFudHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRpc2hlcyIsInBvc3Q6cmVzdGF1cmFudHMiXX0.uaSkDPd5bsrw07_SvnJbxUFF3jqyS07RLZbVXdoiEE-vgPlAkOh8LRUDNsiIoY668PVDUyYf2MZk3WbUzv8GFV14YWdFSFDKN5Ftphsj7J2nHCfLngky-4mWaok-q6ROnLZzNFZfWEQkkDXQy0iz-Jjob3dDD4WnT27vBzqNtAlphzCzKJ_14eKdtNVTs68IyQJ91rjvCLiyM5PQ6xYr4TKMOQAgiBWJ-IrEXuDY-pudglLWu4zgIT1O9SATg3xFi2pkAjL76_uKFyNfKQu7D-svbnZDVIXPtuDte9wfDswDIej9HhSUVBOH5G1kmJB8Tdnb34i4wk-QccVTytY3sA"
USER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NDg2NDVjNmRiYzkwZDNkZTJkMDdjIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkxNDE0MjgzLCJleHAiOjE1OTE1MDA2ODMsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTpkaXNoZXMiLCJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6ZGlzaGVzIiwicGF0Y2g6cmVzdGF1cmFudHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRpc2hlcyIsInBvc3Q6cmVzdGF1cmFudHMiXX0.lRBpIwiWPw9daexOeApjoRRF7utGLh_Rdz-omdoApo-5FGmknljQopDbz5FynV8yMG94cOh-sh13FXeITxi_p0S9K6bDz0DsDeFrU7mwqBBBmpnegL5Lfldf4qrILX0oVe-TXdnQXP85f1bzA_xiUdYg1h306ox1SKs2Nh1puiC7RuXNStdv6KQPCcIO3CDjugtMUSifPREkJe9TXZHhRdW4_YBxJEBBDFDJP4Zsp9gZL21kj4F9w5HAk0NbjBKeRV-jtpreaskCJPk7Gi_jwppSGNZ4ZeXX9eNb9yDXWOsPXlTcfkq3uFMFe7iO7qcfEdLufwQH4-IkaOJOwHD8jQ"

class WhatToEatTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "dish_test"
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
    
    # ### TEST ADMIN ROLE
    # # Test admin post categories
    def test_add_categories_admin(self):
        res = self.client().post('/categories', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_405_add_categories_admin(self):
        category_id = 1000
        res = self.client().post('/categories/' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_delete_dishes_admin(self):
        dish_id = 19
        res = self.client().delete('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_dishes_admin(self):
        dish_id = 1000
        res = self.client().delete('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_delete_categories_admin(self):
        category_id = 10
        res = self.client().delete('/categories/' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_404_delete_categories_admin(self):
        category_id = 10000
        res = self.client().delete('/categories/' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_delete_restaurants_admin(self):
        restaurant_id = 4
        res = self.client().delete('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_404_delete_restaurants_admin(self):
        restaurant_id = 10000
        res = self.client().delete('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # #Test admin get categories
    def test_get_categories_admin(self):
        res = self.client().get("/categories", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
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

    def test_404_patch_category_admin(self):
        category_id = 10000
        res = self.client().patch('/categories/' + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'category':'Spanish'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_restaurants_admin(self):
        res = self.client().post('/restaurants', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_restaurants)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_405_add_restaurants_admin(self):
        restaurant_id = 10000
        res = self.client().post('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_restaurants)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_restaurants_admin(self):
        res = self.client().get("/restaurants", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['restaurants'])
    
    def test_404_get_restaurants_admin(self):
        res_id = 10000
        res = self.client().get("/restaurants/" + str(res_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code, 404)

    def test_patch_restaurants_admin(self):
        restaurant_id = 1
        res = self.client().patch('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'city':'New York Patch Test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_404_patch_restaurants_admin(self):
        restaurant_id = 10000
        res = self.client().patch('/restaurants/' + str(restaurant_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'city':'New York Patch Test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_dishes_admin(self):
        res = self.client().post('/dishes', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_dishes)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_405_add_dishes_admin(self):
        dish_id = 10000
        res = self.client().post('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json=self.new_dishes)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
    
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
    
    def test_patch_dishes_admin(self):
        dish_id = 5
        res = self.client().patch('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'rating':5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_404_patch_dishes_admin(self):
        dish_id = 10000
        res = self.client().patch('/dishes/' + str(dish_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(ADMIN_TOKEN)}, json={'rating':5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    #     ### TEST USER ROLE
    # Test user post categories
    def test_403__add_categories_user(self):
        res = self.client().post('/categories', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)}, json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    # #Test user get categories
    def test_get_categories_user(self):
        res = self.client().get("/categories", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
    
    def test_404_get_categories_user(self):
        category_id = 10000
        res = self.client().get("/categories/" + str(category_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_get_restaurants_user(self):
        res = self.client().get("/restaurants", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
    
    def test_404_get_restaurants_user(self):
        res_id = 10000
        res = self.client().get("/restaurants/" + str(res_id), headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code, 404)
    
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
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

        
