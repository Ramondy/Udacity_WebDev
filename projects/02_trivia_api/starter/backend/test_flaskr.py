import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_user = os.getenv('DBUSER')
        self.database_pw = os.getenv('DBPW')
        self.database_host = os.getenv('DBHOST')
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.database_user, self.database_pw,
                                                               self.database_host, self.database_name)
        self.new_question = {
            "search": False,
            "question": "what is love?",
            "answer": "baby don't hurt me, no more",
            "category": "5",
            "difficulty": "1"
        }

        self.get_question_start = {
            "previous_questions": [],
            "quiz_category": {"id": 1}
        }

        self.get_question_end = {
            "previous_questions": [],
            "quiz_category": {"id": 1}
        }

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each endpoint for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    def test_search_questions(self):
        res = self.client().post('/questions', json={'search': True, 'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])

    def test_404_search_questions(self):
        res = self.client().post('/questions', json={'search': True, 'searchTerm': 'bingpot'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_id'])

        return data['created_id']

    def test_405_post_question(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], str(1))

    def test_400_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_question(self):

        id = self.test_post_question()

        res = self.client().delete('/questions/'+str(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted_id'])

    def test_404_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_next_question_start(self):
        res = self.client().post('/quizzes', json=self.get_question_start)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_get_next_question_end(self):
        stop = False

        while not stop:
            res = self.client().post('/quizzes', json=self.get_question_end)
            data = json.loads(res.data)

            if data['question'] is None:
                stop = True
                self.assertEqual(res.status_code, 200)

            else:
                self.get_question_end['previous_questions'].append(data['question']['id'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()