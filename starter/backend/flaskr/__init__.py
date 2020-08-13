import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import desc, not_
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = page * QUESTIONS_PER_PAGE

    question = [question.format() for question in selection]
    current_question = question[start:end]
    return current_question


def get_category(current_question):
    question_category = [category['category'] for category in current_question]
    for category in question_category:
        category = Category.query.get(category)
        return category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs -- DONE?
'''

    '''
@TODO: Use the after_request decorator to set Access-Control-Allow -- DONE
'''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

        return response

    '''
@TODO: 
Create an endpoint to handle GET requests 
for all available categories. DONE***********
'''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            formatted_categories = {category.id: category.type for category in Category.query.all()}
            if formatted_categories is None:
                abort(404)  # next lesson to handle errors! TODO
            else:
                return jsonify({
                    "success": True,
                    "total_categories": len(formatted_categories),
                    "categories": formatted_categories  # consider peaginment lesson flask part 2 DONE
                })
        except:
            abort(404)


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

    @app.route('/questions', methods=['GET'])
    def get_questions():
        # retruns all questions paginated if pages does not exists it returns 404
        try:
            questions = Question.query.all()
            current_question = paginate_questions(request, questions)

            if not current_question:  # handle errors incase the page entered does not exist
                abort(404)

            if current_question:
                question_category = get_category(current_question)
                formatted_categories = {category.id: category.type for category in Category.query.all()}

                return jsonify({
                    "success": True,
                    "questions": current_question,
                    "total_questions": len(Question.query.all()),
                    "categories": formatted_categories,
                    "current_category": question_category.type,

                })
        except:
            abort(404)

    '''
@TODO: 
Create an endpoint to DELETE question using a question ID. 

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page. 
'''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # deletes question, and returns deleted question id, if it could not find question it returns 404

        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if not question:
                abort(404)
            if (request.method == 'DELETE'):
                question.delete()
            return jsonify({
                "success": True,
                "deleted": question.id,
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

    @app.route('/questions', methods=['POST'])
    def create_question():
        # creates question, and checks if json form values are empty, if empty or it returns 422

        if ((request.json.get('question') == '') | (request.json.get('answer') == '') | (
                request.json.get('difficulty') == '') | (request.json.get('category') == '')):
            return abort(422)

        try:
            new_question = Question(
                question=request.json.get('question'),
                answer=request.json.get('answer'),
                difficulty=request.json.get('difficulty'),
                category=request.json.get('category')

            )

            new_question.insert()
            return jsonify({
                "success": True,
                "created": new_question.id,
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
    def search_question():
        # searches for a question passed in json 'searchTerm' and filters questions from db and formats results

        try:
            search_term = request.json.get('searchTerm')

            question = Question.query.filter(Question.question.ilike(r"%{}%".format(search_term))).all()
            result = [questions.format() for questions in question]
            result_category = get_category(result)

            return jsonify({
                "success": True,
                "questions": result,
                "total_questions": len(result),
                "current_category": result_category.type
            })

        except:

            abort(404)

    '''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def question_category(category_id):
        # retreieves all questions in specific category, returns it formatted. it filters category id and gets all questions
        try:

            questions = Question.query.filter(Question.category == str(category_id)).all()
            formatted_questions = [question.format() for question in questions]
            result_category = get_category(
                formatted_questions)

            return jsonify({
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(formatted_questions),
                "current_category": result_category.type
            })
        except:
            abort(404)

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

    def play_by_category(previous, category):
        # check if category is 0 or not, if 0 then get all questions without filtering category,
        # else if category is not 0 then get the category id and filter questions

        if (category != '0'):
            query = Question.query.filter(not_(Question.id.in_(previous))).filter(
                Question.category == str(category)).all()
            if len(Question.query.filter(Question.category == str(category)).all()) == 0:
                abort(404)

            else:
                return query
        elif category == '0':
            return Question.query.filter(not_(Question.id.in_(previous))).all()

    @app.route('/quizzes', methods=['POST'])
    def play():
        try:
            # get category arg to know what is the category id
            category_id = request.args.get("category")
            # get previous question
            json_previous = request.json.get("previous_questions")
            # setup the random question
            random_question = None
            # pass the previous question and category id
            questions = play_by_category(json_previous,
                                         category_id)  # query questions with gotten category id parameter
            # format questions gotten from helper
            formatted_questions = [question.format() for question in
                                   questions]  # loop through questions and format it into list

            # check if questions are done(so that we do not keep reapeating questions when the questions in list are answered
            if (len(formatted_questions) == 0):
                random_question = None
            else:
                # randomize formmated_questions before returning
                random_question = random.choice(formatted_questions)

            return jsonify({
                "success": True,
                "question": random_question

            })
        except:
            abort(404)

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
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app


if __name__ == "__main__":
    create_app().run()
