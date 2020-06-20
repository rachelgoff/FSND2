import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS

from backend.src.database.models import setup_db, Dish, Restaurant, Category
from backend.src.auth.auth import AuthError, requires_auth
import random


def create_app():
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins.
    '''
    CORS(app, resource={r"*/api/*": {"origins": "*"}})

    '''
    Use the after_request decorator to set Access-Control-Allow.
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    def get_formatted_dish(dish_id):
        formatted_dish = {}
        dish = Dish.query.get(dish_id)
        if dish is None:
            abort(404)
        try:
            dish_category = Category.query.get(dish.category_id)
            dish_restaurant = Restaurant.query.get(dish.restaurant_id)

            formatted_dish = {
                'id': dish.id,
                'name': dish.name,
                'restaurant_id': dish.restaurant_id,
                'category_id': dish.category_id,
                'rating': dish.rating,
                'price': float(dish.price),
                'image_link': dish.image_link,
                'restaurant_name': dish_restaurant.name,
                'category_name': dish_category.name
            }
            return formatted_dish
        except Exception:
            abort(422)

    @app.route('/')
    def hello_what_to_eat():
        return 'Hello, What To Eat!'

    '''
    GET /dishes
    '''
    @app.route('/dishes', methods=['GET'])
    def get_dishes():
        all_dishes = Dish.query.order_by('id').all()
        if all_dishes is None:
            abort(404)
        try:
            formatted_all_dishes = [dish.format() for dish in all_dishes]

            return jsonify({
                "success": True,
                "dishes": formatted_all_dishes
            })
        except Exception:
            abort(404)

    @app.route('/dishes', methods=['POST'])
    @requires_auth("post:dishes")
    def create_dish(token):
        body = request.get_json()
        if body is None:
            abort(400)
        try:
            new_name = body.get('name')
            new_restaurant_id = body.get('restaurant_id')
            new_category_id = body.get('category_id')
            new_rating = body.get('rating')
            new_price = body.get('price')
            new_image_link = body.get('image_link')

            new_dish = Dish(
                name=new_name, restaurant_id=new_restaurant_id,
                category_id=new_category_id, rating=new_rating,
                price=new_price, image_link=new_image_link)
            new_dish.insert()

            all_dishes = Dish.query.order_by('id').all()
            formatted_all_dishes = [dish.format() for dish in all_dishes]

            return jsonify({
                "success": True,
                "new_dish": new_dish.format()
            })
        except Exception:
            abort(422)

    '''
    GET /dishes/<dish_id>
    '''
    @app.route('/dishes/<int:dish_id>', methods=['GET'])
    def get_dish_item(dish_id):
        formatted_dish = get_formatted_dish(dish_id)
        if formatted_dish is None:
            abort(404)

        return jsonify({
                "success": True,
                "dish": formatted_dish
        })

    '''
    PATCH /dishes/<dish_id>
    It requrires 'patch:dishes" permission.
    '''
    @app.route('/dishes/<int:dish_id>', methods=['PATCH'])
    @requires_auth("patch:dishes")
    def update_dish(token, dish_id):
        body = request.get_json()
        if body is None:
            abort(400)
        try:
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
        except Exception:
            abort(404)

    '''
    DELETE /dishes/<dish_id>
    It requrires 'delete:dishes" permission.
    '''
    @app.route('/dishes/<int:dish_id>', methods=['DELETE'])
    @requires_auth("delete:dishes")
    def delete_dish(token, dish_id):
        delete_dish_id = dish_id
        dish = Dish.query.get(dish_id)
        if dish is None:
            abort(404)
        try:
            dish.delete()
            return jsonify({
                "success": True,
                "deleted_dish_id": delete_dish_id
                })
        except Exception:
            abort(422)

    '''
    POST /dishes/search
    It returns dishes that match search query.
    '''
    @app.route('/dishes/search', methods=['POST'])
    def search_dish():
        dishes = []
        body = request.get_json()
        if body is None:
            abort(400)
        try:
            search = body.get('search_term')
            if search is None:
                abort(404)
            search_results = Dish.query.filter(
                Dish.name.ilike("%" + search + "%"))
            for result in search_results:
                dish = get_formatted_dish(result.id)
                dishes.append(dish)
            return jsonify({
                "success": True,
                "dishes": dishes
            })
        except Exception:
            abort(422)

    '''
    GET /categories/<category_id>/dishes
    It returns a list of dishes grouped by the same category.
    '''
    @app.route('/categories/<int:category_id>/dishes', methods=['GET'])
    def dishes_by_categories(category_id):
        dishes_by_categories = []
        dishes = Dish.query.filter_by(category_id=category_id).all()
        if dishes is None:
            abort(404)
        try:
            for d in dishes:
                dish = get_formatted_dish(d.id)
                dishes_by_categories.append(dish)
            return jsonify({
                "success": True,
                "dishes_by_categories": dishes_by_categories
            })
        except Exception:
            abort(422)

    '''
    POST /dishes/recommended
    It returned a recommended dish with the category
    that is specified by users and is not from
    the provided list of the previous dish ids.
    '''
    @app.route('/dishes/recommended', methods=['POST'])
    def recommend_new_dishes():
        recommended_dishes = []
        body = request.get_json()
        if body is None:
            abort(400)
        previous_dishes = body.get('previous_dishes')
        if len(previous_dishes) == 0:
            abort(400)
        new_category = body.get('new_category')
        if new_category is None:
            abort(400)
        try:
            # if not specify a category, then recommend a dish
            # that is not from previous dishes and
            # ratings is greater than or equal to 3.
            if new_category == 0:
                dishes = Dish.query.filter(Dish.id.notin_(
                    previous_dishes), Dish.rating >= 3).order_by(
                        func.random()).limit(1)
                for d in dishes:
                    dish = get_formatted_dish(d.id)
                    recommended_dishes.append(dish)
            else:
                # If users specify a category, then recommend a dish
                # that is from this category, not from previous dishes
                # and ratings is greater than or equal to 3.
                dishes = Dish.query.filter(
                    Dish.category_id == new_category, Dish.id.notin_(
                        previous_dishes), Dish.rating >= 3).order_by(
                            func.random()).limit(1)
                for d in dishes:
                    dish = get_formatted_dish(d.id)
                    recommended_dishes.append(dish)
            return jsonify({
                "success": True,
                "recommended_dish": recommended_dishes[0]
            })
        except Exception:
            abort(422)

    '''
    GET /categories
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        all_categories = Category.query.order_by('id').all()
        if all_categories is None:
            abort(404)
        try:
            formatted_all_categories = [
                category.format() for category in all_categories]

            return jsonify({
                "success": True,
                "categories": formatted_all_categories
            })
        except Exception:
            abort(422)

    '''
    POST /categories
    It requires 'post:categories' permission.
    '''
    @app.route('/categories', methods=['POST'])
    @requires_auth("post:categories")
    def create_category(token):
        body = request.get_json()
        if body is None:
            abort(400)
        new_name = body.get('name')
        if new_name is None:
            abort(404)
        try:
            category = Category(name=new_name)
            category.insert()

            return jsonify({
                "success": True,
                "new_category": category.format()
            })
        except Exception:
            abort(422)

    '''
    PATCH /categories/<category_id>
    It requires 'patch:categories' permission.
    '''
    @app.route('/categories/<int:category_id>', methods=['PATCH'])
    @requires_auth("patch:categories")
    def update_category(token, category_id):
        body = request.get_json()
        if body is None:
            abort(400)
        new_name = body.get('name')
        if new_name is None:
            abort(404)

        category_item = Category.query.get(category_id)
        if category_item is None:
            abort(404)
        try:
            category_item.name = new_name
            category_item.update()
            return jsonify({
                "success": True,
                "updated_category": category_item.format()
            })
        except Exception:
            abort(422)

    '''
    GET /categories/<category_id>
    '''
    @app.route('/categories/<int:category_id>', methods=['GET'])
    def get_category_by_id(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        return jsonify({
            "success": True,
            "category": category.format()
        })

    '''
    DELETE /categories/<category_id>
    It requires 'delete:categories' permission.
    '''
    @app.route('/categories/<int:category_id>', methods=['DELETE'])
    @requires_auth("delete:categories")
    def delete_category(token, category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        delete_id = category_id
        try:
            category.delete()

            return jsonify({
                "success": True,
                "delete_category_id": delete_id,
            })
        except Exception:
            abort(422)

    '''
    GET /restaurants
    '''
    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        all_restaurants = Restaurant.query.order_by('id').all()
        if all_restaurants is None:
            abort(404)
        try:
            formatted_all_restaurants = [
                restaurant.format() for restaurant in all_restaurants]
            return jsonify({
                "success": True,
                "restaurants": formatted_all_restaurants
            })
        except Exception:
            abort(422)

    '''
    GET /restaurants/<restaurant_id>/dishes
    It returns a list of dishes from the same restaurant.
    '''
    @app.route('/restaurants/<int:restaurant_id>/dishes', methods=['GET'])
    def dishes_by_restaurants(restaurant_id):
        dishes_by_restaurants = []
        dishes = Dish.query.filter_by(restaurant_id=restaurant_id).all()
        if dishes is None:
            abort(404)
        try:
            for d in dishes:
                dish = get_formatted_dish(d.id)
                dishes_by_restaurants.append(dish)
            return jsonify({
                "success": True,
                "dishes_by_restaurants": dishes_by_restaurants
            })
        except Exception:
            abort(422)

    '''
    POST /restaurants
    It requires 'post:restaurants' permission.
    '''
    @app.route('/restaurants', methods=['POST'])
    @requires_auth("post:restaurants")
    def create_restaurant(token):
        body = request.get_json()
        if body is None:
            abort(400)
        new_name = body.get('name')
        new_city = body.get('city')
        new_addr = body.get('address')
        new_state = body.get('state')
        new_r_image_link = body.get('r_image_link')
        new_website = body.get('website')

        # new_r_image_link, new_website can be null
        if any(arg is None for arg in [
            new_name, new_city, new_addr,
            new_state, new_r_image_link, new_website
                ]) or '' in [new_name, new_city, new_addr, new_state]:
            abort(400)
        try:
            new_restaurant = Restaurant(
                name=new_name, city=new_city, state=new_state,
                address=new_addr, r_image_link=new_r_image_link,
                website=new_website)
            new_restaurant.insert()

            return jsonify({
                "success": True,
                "new_restaurant": new_restaurant.format()
            })
        except Exception:
            abort(422)

    '''
    PATCH /restaurants/<restaurant_id>
    It requires 'patch:restaurants' permission.
    '''
    @app.route('/restaurants/<int:restaurant_id>', methods=['PATCH'])
    @requires_auth("patch:restaurants")
    def update_restaurant(token, restaurant_id):
        body = request.get_json()
        if body is None:
            abort(400)
        new_name = body.get('name')
        new_city = body.get('city')
        new_addr = body.get('address')
        new_state = body.get('state')
        new_r_image_link = body.get('r_image_link')
        new_website = body.get('website')

        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant is None:
            abort(404)
        try:
            if new_name is not None and not '':
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

            return jsonify({
                "success": True,
                "updated_restaurant": restaurant.format()
            })
        except Exception as e:
            abort(404)

    '''
    GET /restaurants/<restaurant_id>
    '''
    @app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
    def get_restaurant_by_id(restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant is None:
            abort(404)
        return jsonify({
            "success": True,
            "restaurant": restaurant.format()
        })

    '''
    DELETE /restaurants/<restaurant_id>
    It requires 'delete:restaurants' permission.
    '''
    @app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
    @requires_auth("delete:restaurants")
    def delete_restaurant_by_id(token, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant is None:
            abort(404)
        try:
            deleted_id = restaurant_id
            restaurant.delete()

            return jsonify({
                "success": True,
                "deleted_restaurant_id": deleted_id,
            })
        except Exception:
            abort(422)

    '''
    Error Handling
    '''
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

    @app.errorhandler(400)
    def unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
            }), 400

    return app

    app = create_app()

    if __name__ == '__main__':
        # port = int(os.environ.get('PORT', 5000))
        app.run()
        # print("Started server on port 5000")
