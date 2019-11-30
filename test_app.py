import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Actor, Movie, actors


class CastingAgencyTestCase(unittest.TestCase):
   
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','e2806387','localhost:5432', self.database_name)
        self.casting_assistant = ''
        self.executive_producer = ''
        self.casting_director= ''
        setup_db(self.app, self.database_path) 
    
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_actors_casting_assistant(self):
        response = self.client().get('/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['actors'])

    def test_get_movies_casting_assistant(self):
        response = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['movies'])




if __name__ == '__main__':
    unittest.main()