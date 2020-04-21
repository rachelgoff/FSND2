import os
from flask import Flask, request, abort, jsonify
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
#CORS(app)
CORS(app, resource={r"*/api/*": {"origins": "*"}})

'''
Use the after_request decorator to set Access-Control-Allow.
'''
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        all_drinks = Drink.query.order_by('id').all()
        drinks = [drink.short() for drink in all_drinks]
        print(drinks)

        return jsonify({
            "success": True,
            "drinks": drinks
            })
    except:
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth("get:drinks-detail")
def get_drinks_detail(token):
    try:
        all_drinks = Drink.query.order_by('id').all()
        drinks = [drink.long() for drink in all_drinks]
        print(drinks)

        return jsonify({
            "success": True,
            "drinks": drinks
            })
    except:
        abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def create_drink(token):
    try:
        body = request.get_json()
        title = body.get('title')
        recipe = body.get('recipe')
        #parts = recipe['parts']
        #color = recipe['color']
        #name = recipe['name']

        if (title is None) or (recipe is None):
            abort(422)

        new_drink = Drink(title=title, recipe=json.dumps([recipe]))
        new_drink.insert()
        print(new_drink.id)

        all_drinks = Drink.query.all()
        drinks = [drink.long() for drink in all_drinks]
        drink = Drink.query.get(1)
        print(drink.long())

        return jsonify({
            "success": True,
            "drinks": drinks
            })
    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
# '''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def update_drink(token, id):
    body = request.get_json()
    new_title = body.get('title')
    new_recipe = body.get('recipe')

    drink = Drink.query.get(id)
    if drink == None:
        abort(404)
    if new_title != None:
        drink.title = new_title
    if new_recipe != None:
        drink.recipe = new_recipe

    drink.update()

    return jsonify({
        "success": True,
        "drinks": drink.long()
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth("delete:drinks")
def delete_drink(toke, id):
    try:
        delete_id = id
        drink = Drink.query.get(id)
        if drink == None:
            abort(404)
        drink.delete()

        return jsonify({
            "success": True,
            "delete": delete_id
        })
    except:
        abort(404)
## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
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
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Unauthorized error"
        }), 401

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
