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