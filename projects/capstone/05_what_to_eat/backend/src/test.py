import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .app import create_app
from .database.models import setup_db, Dish, Restaurant, Category

ADMIN_TOKEN = os.environ['ADMIN_TOKEN']
USER_TOKEN = os.environ['USER_TOKEN']

'''
This class represents the What To Eat test case.
'''


class WhatToEatTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "dish_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Binds the app to the current context.
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        # Prepare new_dishes, new_categories and new_restaurants for testing.
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
        pass

    '''
    TEST ADMIN ROLE
    '''

    '''
    Test Admin post categories
    '''
    def test_add_categories_admin(self):
        res = self.client().post('/categories', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_add_categories_admin(self):
        category_id = 1000
        res = self.client().post('/categories/' + str(category_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json=self.new_categories)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    '''
    Test Admin delete dishes
    '''
    def test_delete_dishes_admin(self):
        dish_id = 19
        res = self.client().delete('/dishes/' + str(dish_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_dishes_admin(self):
        dish_id = 1000
        res = self.client().delete('/dishes/' + str(dish_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test Admin delete categories
    '''
    def test_delete_categories_admin(self):
        category_id = 10
        res = self.client().delete('/categories/' + str(category_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_categories_admin(self):
        category_id = 10000
        res = self.client().delete('/categories/' + str(category_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test Admin delete restaurants
    '''
    def test_delete_restaurants_admin(self):
        restaurant_id = 4
        res = self.client().delete('/restaurants/' + str(
            restaurant_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_restaurants_admin(self):
        restaurant_id = 10000
        res = self.client().delete('/restaurants/' + str(
            restaurant_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test Admin get categories
    '''
    def test_get_categories_admin(self):
        res = self.client().get("/categories", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_404_get_categories_admin(self):
        res = self.client().get("/categories/10000", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test Admin patch categories
    '''
    def test_patch_category_admin(self):
        category_id = 1
        res = self.client().patch('/categories/' + str(category_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json={'category': 'Spanish'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_category_admin(self):
        category_id = 10000
        res = self.client().patch('/categories/' + str(category_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json={'category': 'Spanish'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test Admin add restaurants
    '''
    def test_add_restaurants_admin(self):
        res = self.client().post('/restaurants', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json=self.new_restaurants)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_add_restaurants_admin(self):
        restaurant_id = 10000
        res = self.client().post('/restaurants/' + str(
            restaurant_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json=self.new_restaurants)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    '''
    Test Admin get restaurants
    '''
    def test_get_restaurants_admin(self):
        res = self.client().get("/restaurants", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['restaurants'])

    def test_404_get_restaurants_admin(self):
        res_id = 10000
        res = self.client().get("/restaurants/" + str(res_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test Admin patch restaurants
    '''
    def test_patch_restaurants_admin(self):
        restaurant_id = 1
        res = self.client().patch('/restaurants/' + str(
            restaurant_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json={'city': 'New York Patch Test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_restaurants_admin(self):
        restaurant_id = 10000
        res = self.client().patch('/restaurants/' + str(
            restaurant_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json={'city': 'New York Patch Test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test Admin add dishes
    '''
    def test_add_dishes_admin(self):
        res = self.client().post('/dishes', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json=self.new_dishes)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_add_dishes_admin(self):
        dish_id = 10000
        res = self.client().post('/dishes/' + str(dish_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json=self.new_dishes)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    '''
    Test Admin get dishes
    '''
    def test_get_dishes_admin(self):
        res = self.client().get("/dishes", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['dishes'])

    def test_404_get_dishes_admin(self):
        dish_id = 10000
        res = self.client().get("/dishes/" + str(dish_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test Admin patch dishes
    '''
    def test_patch_dishes_admin(self):
        dish_id = 5
        res = self.client().patch('/dishes/' + str(dish_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json={'rating': 5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_dishes_admin(self):
        dish_id = 10000
        res = self.client().patch('/dishes/' + str(dish_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(ADMIN_TOKEN)},
            json={'rating': 5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    TEST USER ROLE
    '''

    '''
    Test User get categories
    '''
    def test_get_categories_user(self):
        res = self.client().get("/categories", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    '''
    Test User get categories which doesn't exist
    '''
    def test_404_get_categories_user(self):
        category_id = 10000
        res = self.client().get("/categories/" + str(category_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test User get restaurants
    '''
    def test_get_restaurants_user(self):
        res = self.client().get("/restaurants", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_404_get_restaurants_user(self):
        res_id = 10000
        res = self.client().get("/restaurants/" + str(res_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test User get dishes
    '''
    def test_get_dishes_user(self):
        res = self.client().get("/dishes", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['dishes'])

    def test_404_get_dishes_user(self):
        dish_id = 10000
        res = self.client().get("/dishes/" + str(dish_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(USER_TOKEN)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)


'''
Make the tests conveniently executable
'''

if __name__ == "__main__":
    unittest.main()
