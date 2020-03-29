import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app, resource={r"*/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response

  def paginated_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]
    current_questions = formatted_questions[start:end]
    print(current_questions)

    return current_questions

  def get_questions_by_category(category_id):
    questions_by_categories = Question.query.filter_by(category=category_id).all()
    formatted_questions_by_categories = [question.format() for question in questions_by_categories]

    return formatted_questions_by_categories

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return jsonify({
      'success': True,
      'categories': formatted_categories
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  #Chrome will redirect with trailing slash automatically. Added two decorators to resolve different browsers behavior issue.
  @app.route('/questions/')
  @app.route('/questions') 
  def get_questions():
    category_list = []
    category_type = ''

    try:
      questions = Question.query.order_by('id').all()
      current_questions = paginated_questions(request, questions)
    except:
      abort(400)

    if len(current_questions) == 0:
      abort(404)
    else:
      categories = Category.query.all()
      for category in categories:
        category_list.append(category.type)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'number of total questions': len(current_questions),
        'current category': '',
        'categories': category_list
        })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        return jsonify({
          "success": False
          })
      
      question.delete()
      questions = Question.query.order_by('id').all()
      current_questions = paginated_questions(request, questions)

      return jsonify({
          "success": True,
          "deleted question id": question_id,
          "current questions": current_questions,
          "total questions": len(questions)
          })
    except:
      abort(404)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions/', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question')
    new_answer = body.get('answer')
    new_category = body.get('category')
    new_difficulty = body.get('difficulty')

    try:
      new_question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      new_question.insert()
      questions = Question.query.order_by('id').all()
      current_questions = paginated_questions(request, questions)

      return jsonify({
          "success": True,
          "question id": new_question.id,
          "current questions": current_questions,
          "total questions": len(questions)
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    try:
      body = request.get_json()
      searchTerm = body.get('searchTerm')
      search_results = Question.query.filter(Question.question.ilike("%" + searchTerm + "%"))
      formatted_matched_questions = [search_result.format() for search_result in search_results]

      questions = Question.query.order_by('id').all()
      formatted_total_questions = [question.format() for question in questions]

      result = {
          "questions": formatted_matched_questions,
          "total_questions": formatted_total_questions,
          "current category": formatted_matched_questions[0]['category'],
          "current question":formatted_matched_questions[0]
      }

      return jsonify({
          'success': True,
          'result': result
        })
    except:
      abort(400)


  '''

  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_by_category(category_id):
      try:
          questions_by_categories = Question.query.filter_by(category=category_id).all()
          formatted_questions_by_categories = [question.format() for question in questions_by_categories]

          total_questions = Question.query.order_by('id').all()
          formatted_total_questions = [question.format() for question in total_questions]

          result = {
              "questions": formatted_questions_by_categories,
              "total_questions": formatted_total_questions,
              "current category": formatted_questions_by_categories[0]['category']
          }

          return jsonify({
            'success': True,
            'result': result
            })
      except:
        abort(400)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    try:
      body = request.get_json()
      previous_questions = body.get('previous_questions')
      quiz_category = body.get('quiz_category')

      next_questions = Question.query.filter(Question.category == quiz_category, Question.id.notin_(previous_questions)).order_by(func.random()).limit(1)
      formatted_next_questions = [question.format() for question in next_questions]

      if len(formatted_next_questions) > 0:
        return jsonify({
          'success': True,
          'new_question': formatted_next_questions
          })
      else:
        return jsonify({
          'success': False
          })

    except:
      abort(400)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
      }), 400

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable entity"
      }), 422










  
  return app

    