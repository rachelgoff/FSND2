import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS

from .database.models import setup_db, Dish, Restaurant, Category
# from .database import models

# debug
print("Imported database from models")
print("Before models.setup_db")

def create_app():
    app = Flask(__name__)
    setup_db(app)

    # debug
    print("Finished running models.setup_db")

    CORS(app, resource={r"*/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    default_dish_image_link = "https://unsplash.com/photos/1Rm9GLHV0UA"
    default_restaurant_image_link = "https://unsplash.com/photos/26T6EAsQCiA"
    
    def get_formatted_dish(dish_id):
        formatted_dish = {}
        try:
            dish = Dish.query.get(dish_id)
            if dish is None:
                abort(404)
        except Exception as e:
            print(e)
            abort(404)

        dish_category = Category.query.get(dish.category_id)
        dish_restaurant = Restaurant.query.get(dish.restaurant_id)

        formatted_dish = {
            'id': dish.id,
            'name': dish.name,
            'restaurant_id': dish.restaurant_id,
            'category_id': dish.category_id,
            'rating': dish.rating,
            'price': float(dish.price),
            'image_link': dish.image_link or default_dish_image_link,
            'restaurant_name': dish_restaurant.name,
            'category': dish_category.category
        }
        return formatted_dish

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/dishes', methods=['GET'])
    def get_dishes():
        try:
            all_dishes = Dish.query.order_by('id').all()
            print(all_dishes)
            formatted_all_dishes = [dish.format() for dish in all_dishes]
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "dishes": formatted_all_dishes
        })

    @app.route('/dishes', methods=['POST'])
    def create_dish():
        body = request.get_json()
        new_name = body.get('name')
        new_restaurant_id = body.get('restaurant_id')
        new_category_id = body.get('category_id')
        new_rating = body.get('rating')
        new_price = body.get('price')
        new_image_link = body.get('image_link')
        
        new_dish = Dish(name=new_name, restaurant_id=new_restaurant_id, category_id=new_category_id, rating=new_rating, price=new_price, image_link=new_image_link)
        new_dish.insert()

        all_dishes = Dish.query.order_by('id').all()
        formatted_all_dishes = [dish.format() for dish in all_dishes]

        return jsonify({
            "success": True,
            "new_dish": new_dish.format(),
            "dishes": formatted_all_dishes
        })
    
    @app.route('/dishes/<int:dish_id>', methods=['GET'])
    def get_dish_item(dish_id):        
        formatted_dish = get_formatted_dish(dish_id)
        # formatted_dish = {}
        # try:
        #     dish = Dish.query.get(dish_id)
        #     if dish is None:
        #         abort(404)
        # except Exception as e:
        #     print(e)
        #     abort(404)

        # dish_category = Category.query.get(dish.category_id)
        # dish_restaurant = Restaurant.query.get(dish.restaurant_id)

        # formatted_dish = {
        #     'id': dish.id,
        #     'name': dish.name,
        #     'restaurant_id': dish.restaurant_id,
        #     'category_id': dish.category_id,
        #     'rating': dish.rating,
        #     'price': float(dish.price),
        #     'image_link': dish.image_link or default_dish_image_link,
        #     'restaurant_name': dish_restaurant.name,
        #     'category': dish_category.category
        # }
        return jsonify({
                "success": True,
                "dish": formatted_dish
            })

    @app.route('/dishes/<int:dish_id>', methods=['PATCH'])
    def update_dish(dish_id):
        body = request.get_json()
        new_name = body.get('name')
        new_restaurant_id = body.get('restaurant_id')
        new_category_id = body.get('category_id')
        new_rating = body.get('rating')
        new_price = body.get('price')
        new_image_link = body.get('image_link')

        dish = Dish.query.get(dish_id)

        if dish is None:
            abort(404)
        if new_name is not None:
            dish.name = new_name
        if new_restaurant_id is not None:
            dish.restaurant_id = new_restaurant_id
        if new_category_id is not None:
            dish.category_id = new_category_id
        if new_rating is not None:
            dish.rating = new_rating
        if new_price is not None:
            dish.price = new_price
        if new_image_link is not None:
            dish.image_link = new_image_link

        dish.update()

        new_dish = get_formatted_dish(dish_id)

        return jsonify({
                "success": True,
                "dish": new_dish
            })

    @app.route('/dishes/<int:dish_id>', methods=['DELETE'])
    def delete_dish(dish_id):
        try:
            delete_dish_id = dish_id
            dish = Dish.query.get(dish_id)
            #print(dish)
        # except Exception as e:
        #     print(e)
        #     abort(404)
            print(dish)
            if dish is None:
                abort(404)
            dish.delete()
            return jsonify({
                    "success": True,
                    "deleted dish": delete_dish_id
                })
        except IndexError:
             abort(404)



    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            all_categories = Category.query.order_by('id').all()
            formatted_all_categories = [category.format() for category in all_categories]
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "categories": formatted_all_categories
        })

    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        try:
            all_restaurants = Restaurant.query.order_by('id').all()
            formatted_all_restaurants = [restaurant.format() for restaurant in all_restaurants]
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "restaurants": formatted_all_restaurants
        })

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
            }), 404

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='127.0.0.1', port=port)
        print("Started server on port 5000")
    return app