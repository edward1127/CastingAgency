import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, movies


TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT')
CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR')
EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.casting_assistant = CASTING_ASSISTANT
        self.casting_director = CASTING_DIRECTOR
        self.executive_producer = EXECUTIVE_PRODUCER
        setup_db(self.app, TEST_DATABASE_URI)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    '''
    RBAC TEST
    '''

    def test_post_actors_by_executive_producer_with_auth_200(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "name": "Edward",
                                          "gender": "male",
                                          "age": 25,
                                      })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_post_actors_by_casting_assistant_without_auth_401(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "name": "Edward",
                                          "gender": "male",
                                          "age": 25
                                      })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')

    def test_post_movies_by_executive_producer_with_auth_200(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "title": "Iron Man",
                                          "release_date": "2015-01-01"
                                      })

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_post_movies_by_casting_assistant_without_auth_401(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "title": "Iron Man",
                                          "release_date": "2015-01-01"
                                      })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')

    def test_get_actors_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/actors',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_get_actors_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_get_movies_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/movies',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_get_movies_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_patch_actors_by_casting_director_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_patch_actors_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')

    def test_patch_movies_by_casting_director_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_patch_movies_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')

    def test_delete_actors_by_executive_producer_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_delete_actors_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.casting_assistant)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')

    def test_delete_movies_by_executive_producer_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_delete_movies_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.casting_assistant)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')


if __name__ == '__main__':
    unittest.main()
