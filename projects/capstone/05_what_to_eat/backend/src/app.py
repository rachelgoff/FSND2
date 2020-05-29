import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS

from .database.models import setup_db, Dish, Restaurant, Category

app = Flask(__name__)
setup_db(app)
CORS(app, resource={r"*/api/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/dishes', methods=['GET'])
def get_dishes():
    try:
        all_dishes = Dish.query.order_by('id').all()
    except Exception as e:
        print(e)
        abort(404)
    return jsonify({
        "success": True,
        "dishes": all_dishes
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
