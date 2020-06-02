import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS

from .database.models import setup_db, Dish, Restaurant, Category
# from .database import models
import random

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

    @app.route('/dishes/search', methods=['POST'])
    def search_dish():
        dishes = []
        try:
            body = request.get_json()
            search = body.get('search_term')
            if search is not None:
                search_results = Dish.query.filter(Dish.name.ilike("%" + search + "%"))
                for result in search_results:
                    dish = get_formatted_dish(result.id)
                    dishes.append(dish)
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "dishes": dishes
        })
    
    @app.route('/categories/<int:category_id>/dishes', methods=['GET'])
    def dishes_by_categories(category_id):
        dishes_by_categories = []
        try:
            dishes = Dish.query.filter_by(category_id=category_id).all()
            if dishes is not None:
                for d in dishes:
                    # dish = get_formatted_dish(d.id)
                    # dishes.append(dish)
                    print(d.id)
                    dish = get_formatted_dish(d.id)
                    dishes_by_categories.append(dish)
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "dishes_by_categories": dishes_by_categories
        })
    
    @app.route('/dishes/try', methods=['POST'])
    def try_new_dishes():
        dishes_to_try = []
        try:
            body = request.get_json()
            previous_dishes = body.get('previous_dishes')
            new_category = body.get('new_category')
            if new_category is not None:
                if new_category == 0:
                    dishes = Dish.query.filter(Dish.id.notin_(previous_dishes), Dish.rating>=3).order_by(func.random()).limit(1) # if not specify a category, then recommend a dish that is not from previous dishes and ratings is greater than or equal to 3.
                    for d in dishes:
                        dish = get_formatted_dish(d.id)
                        dishes_to_try.append(dish)
                else:
                    dishes = Dish.query.filter(Dish.category_id==new_category, Dish.id.notin_(previous_dishes), Dish.rating>=3).order_by(func.random()).limit(1) # If specify a category, then recommend a dish that is from this category, not from previous dishes and ratings is greater than or equal to 3.
                    for d in dishes:
                        dish = get_formatted_dish(d.id)
                        dishes_to_try.append(dish)

        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "dish to try": dishes_to_try[0]
        })

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

    @app.route('/categories', methods=['POST'])
    def create_category():
        try:
            body = request.get_json()
            new_category = body.get('category')

            category = Category(category=new_category)
            category.insert()
            categories = Category.query.order_by('id').all()
            formatted_all_categories = [category.format() for category in categories]
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "categories": formatted_all_categories
        })

    @app.route('/categories/<int:category_id>', methods=['GET'])
    def get_category_by_id(category_id):
        try:
            category = Category.query.get(category_id)
            print(category_id)
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "category": category.format()
        })

    @app.route('/categories/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):
        try:
            category = Category.query.get(category_id)
            delete_id = category_id
            category.delete()

            categories = Category.query.order_by('id').all()
            formatted_all_categories = [category.format() for category in categories]
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "delete_id": delete_id,
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

    @app.route('/restaurants/<int:restaurant_id>/dishes', methods=['GET'])
    def dishes_by_restaurants(restaurant_id):
        dishes_by_restaurants = []
        try:
            dishes = Dish.query.filter_by(restaurant_id=restaurant_id).all()
            if dishes is not None:
                for d in dishes:
                    # dish = get_formatted_dish(d.id)
                    # dishes.append(dish)
                    print(d.id)
                    dish = get_formatted_dish(d.id)
                    dishes_by_restaurants.append(dish)
        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "dishes_by_restaurants": dishes_by_restaurants
        })
    
    @app.route('/restaurants', methods=['POST'])
    def create_restaurant():
        try:
            body = request.get_json()
            new_name = body.get('name')
            new_city = body.get('city')
            new_addr = body.get('address')
            new_state = body.get('state')
            new_r_image_link = body.get('r_image_link')
            new_website = body.get('website')

            new_restaurant = Restaurant(name=new_name, city=new_city, state=new_state, address=new_addr, r_image_link=new_r_image_link, website=new_website)
            new_restaurant.insert()

        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "new_restaurant": new_restaurant.format()
        })
    
    @app.route('/restaurants/<int:restaurant_id>', methods=['PATCH'])
    def update_restaurant(restaurant_id):
        try:
            body = request.get_json()
            new_name = body.get('name')
            new_city = body.get('city')
            new_addr = body.get('address')
            new_state = body.get('state')
            new_r_image_link = body.get('r_image_link')
            new_website = body.get('website')

            restaurant = Restaurant.query.get(restaurant_id)

            if new_name is not None:
                restaurant.name = new_name
            if new_city is not None:
                restaurant.city = new_city
            if new_state is not None:
                restaurant.state = new_state
            if new_addr is not None:
                restaurant.address = new_addr
            if new_r_image_link is not None:
                restaurant.r_image_link = new_r_image_link
            if new_website is not None:
                restaurant.website = new_website

            restaurant.update()

        except Exception as e:
            print(e)
            abort(404)
        return jsonify({
            "success": True,
            "updated_restaurant": restaurant.format()
        })


    
    # Error Handling


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422


    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
            }), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
        }), 500


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
        }), 405


    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized error"
            }), 401

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='127.0.0.1', port=port)
        print("Started server on port 5000")
    return app