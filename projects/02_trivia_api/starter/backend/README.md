# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT

## Endpoints
- GET '/categories'
- GET '/questions'
- DELETE '/questions/<int:question_id>'
- GET '/categories/<int:category_id>/questions'
- POST '/questions'
- POST '/quizzes'


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the values are the corresponding string of the category list
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
  
GET '/questions'
- Fetches a dictionary containing a list of paginated questions, the number of questions in the db, the current category, a dict of categories.
- Request Arguments: None
- Returns: An object with four keys
{'questions': list of paginated questions (set to 10 questions per page),
'total_questions': total number of questions in the db,
'categories': dict of categories, similar to the return of the GET '/categories' endpoint
'current_category': None}

DELETE '/questions/<int:question_id>'
- Deletes a question from the db
- Request Arguments: <int:question_id>, indicating the id of the question to delete
- Returns: An object with one key
{'deleted_id': id of the item deleted}

GET '/categories/<int:category_id>/questions'
- Fetches a dictionary containing - for a given category - a list of paginated questions, the number of questions in that category, the current category.
- Request Arguments: <int:category_id>, indicating the id of the selected category 
- Returns: An object with three keys
{'questions': list of paginated questions from the selected category (set to 10 questions per page),
'total_questions': total number of questions in this category,
'current_category': id of the selected category}

POST '/questions'
- Handles both a search on the question set and posting a new question to the db 
- the intent is specified by using a "search" boolean argument
- Request Arguments:
{'search': boolean,
  if search:
    'searchTerm': string
  if not search:
    "question": string, "answer": string, "category": str(int), "difficulty": str(int)
}
- Returns:
  if search: an object with three keys
    {'questions': list of questions containing the searchTerm,
    'total_questions': total number of questions containing the searchTerm,
    'current_category': None}
  if not search: an object with one key
    {'created_id': id of the item created}

POST '/quizzes'
- Fetches a new question from a given category, given a history of previously selected questions - or None if the category is spent
- Request Arguments:
{'previous_questions': a list of question_id of questions already asked,
'quiz_category': a dict {"id": int}, int indicating the category_id from which to select
}
- Returns: An object with one key
{'question': a Question object formatted as a dict  {'id': int, 'question': str, 'answer': str, 'category': str, 'difficulty': str}
or
{'question': None} if the category is spent
  
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```