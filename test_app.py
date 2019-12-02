import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, movies


# login https://cheermoon.auth0.com/authorize?audience=castingagency&response_type=token&client_id=0AclWPWFwUn1rZ0uq22UKyol5CV01GSN&redirect_uri=http://localhost:8100/

TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.casting_assistant = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjZDFmNTg3M2JhMzYwZWQzYTZiMGVhIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTI5Mjk1OSwiZXhwIjoxNTc1MzY0OTU5LCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.uQnuZfPDnyM6h5s-5sddibpBHtPLzZSjQ28L7uquX9JC7swmtWgpm6jtPy-qoPmCAXzCYj2U4s2UxZuNa1AqWX-ARMfguo4mpjdRxEoIAMTcD9eCihWmA5UiRnsgKc3JvCnWB0TojTTNSRthiASq15nDpnIlijtm2wGZ2Vm4sEMEX7w-SQZQiRM2l_CkXU4vT1xHzzIGVcRykbyE1wIOU8R-xdyyiDbOcuPfnmJuy3OJlLxkp17n3HJsKXgn7J9zHcvWFN-7sxEbZA0yhkoMNyo65pnVmhzd4xkq-ba9pcWZ46nNIHe3UGNN8jMB0TGhPhNwcL6amxo_ZtjA6xMxrw'
        self.casting_director = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkMDkxNmFiZmIyOGMwZWNiYTVkNDljIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTI5MjgyMywiZXhwIjoxNTc1MzY0ODIzLCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.NsIatU96ah0nPXtBnNgjVWlMQtouODVA7HqakZexQsyWVu_nBXTMtUbmXNmaBnZWbXyXdRa42BnWK4yuUQGUlrb7hvBXCE4ZsezN8Fiy5NRedK8RdichuI-YS5zBXoMzcLmY5N891dyeCu4F0U0HjsyxfZ7xnmlI-2v_GdW82qOZx-W7d8dXDUV-7oe822qZLG-j2LQfoLcl1EI7xIrwJ5stDsAoj85rLDezD7mr_M4FLpXK5MJ_3RAeQS1ODBzu2LzLRkHYhNMN4UrAvpiS_gFUQUh7lWGZ6l520QiUFmyEQGn_MatRWilfEBGGueW2KNU3oOSzm5qTdwmHjXboHA'
        self.executive_producer = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlMjAyNDY2OGJhZTEwZDJhN2MwNDVlIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTI4NTk0MiwiZXhwIjoxNTc1MzU3OTQyLCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.RvtwYgVR6Va64zf1Ar8i40W3oJGffVWi8tC1OTTLyA5Vb25lhgLZKwBdO-G79wrKdLBK7yZY8IxiM6IM-bMLvOooJz0i0_siarWCFmkp62u9ZEbwzUEt7m1zpkLBokyvSkpt8CNXABwbJl33lQ4ryZseTy6vFWUPuPHxfuIX2t3W0SfkP3sW_QNPtxfbrqBWTCFt3WjV1hWAq6ssUriIKEqns-Aw5EYrhb5RUKtcnnGchdAxRWRgY770Gj9zYKBvXvONc6jzgKUDmOhjI7vxRHkNV-x2HC6Q5bHvQerstZL2odG0tqavhXJLzrEc3L_jF-kyr_0uBDSdBegbJgMB2A'
        setup_db(self.app, TEST_DATABASE_URI)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            


    def test_post_actors_by_executive_producer_with_auth_200(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}".format(self.executive_producer)
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
                                          "Authorization": "Bearer {}".format(self.casting_assistant)
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
                                          "Authorization": "Bearer {}".format(self.executive_producer)
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
                                          "Authorization": "Bearer {}".format(self.casting_assistant)
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
                                         "Authorization": "Bearer {}".format(self.casting_assistant)
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
                                         "Authorization": "Bearer {}".format(self.casting_assistant)
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

    def test_patch_actors_by_casting_director_with_auth_404(self):
        id = 999
        response = self.client().patch('/actors/{}'.format(id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status_message'], "resource Not found")

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

    def test_patch_movies_by_casting_director_with_auth_404(self):
        id = 999
        response = self.client().patch('/movies/{}'.format(id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status_message'], "resource Not found")

    def test_delete_actors_by_executive_producer_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_delete_actors_by_executive_producer_with_auth_404(self):
        id = 999
        response = self.client().delete('actors/{}'.format(id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status_message'], "resource Not found")

    def test_delete_movies_by_executive_producer_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_delete_movies_by_executive_producer_with_auth_404(self):
        id = 999
        response = self.client().delete('movies/{}'.format(id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status_message'], "resource Not found")


if __name__ == '__main__':
    unittest.main()
