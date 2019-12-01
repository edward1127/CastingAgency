import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, movies


# login https://cheermoon.auth0.com/authorize?audience=castingagency&response_type=token&client_id=0AclWPWFwUn1rZ0uq22UKyol5CV01GSN&redirect_uri=http://localhost:8100/

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        self.casting_assistant = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjZDFmNTg3M2JhMzYwZWQzYTZiMGVhIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTE4NjcxNCwiZXhwIjoxNTc1MjU4NzE0LCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.XKYjc0caU5Agpn-X3Pp2gralFv5xRFU6KS12e5fSDbsJv5cNuWF4yNugm22dmUxDl4H-nnbCw3GpXKtm9_pmxzP05HwgIwGlyipn1oOnty42MDcifur6RJtSq6hvByF9s5pRyI3e1lI3CqxUlhTfCHKWYDkEKggSrW9Qnd2Od2G6jaWw4KR5AkdD7ABY8MEsTLo_qyqe4aqX_zhFHLK16GPNRv0AB9LtCaIA7qzfRpwCPG-gggkUMHjVwiUk84Ws8SOL2tKCP_lUiNyHma9ajxVihJLaIajhVk97a2op7W_ELOazbhGBcZVl9QheUamBYaG-X_eo4wAk7zL6lVQ5Vg'
        self.casting_director = ''
        self.executive_producer = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlMjAyNDY2OGJhZTEwZDJhN2MwNDVlIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTE4Njc4MCwiZXhwIjoxNTc1MjU4NzgwLCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.iUzlzpaQNlE2OvJeEqgOuRaqgSTbeAkSJ0NoOaSe7yL7Gd9cQNPXf0AhCZk3siO-3btrH5B09ZmXSWWPmO4ND0H2gRAO_kmJ_2RJRxlLqLc9v72ojVsT71SZ-IGvYj9kEtaP42OgNQCFm8bt5XjUp-0cfrd9lgKfWqLciqi6eZTs_BtlpRjbXGBFCtam3rD1Oq6R_T_d0ye7Dzm_Z2gK_IVhllTJ2Xb_jVeDZpgcfExH27H6TwN_30UWjx0S9X75929XooWKVRqPyUQOiYbnCbHIujFFrVzTRNuTYimdhcUGe2HIIJS3e2bCLPwSnWakbinfR_rurIQ_Oek7aJvS9g'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def test_post_actors_by_executive_producer_with_auth(self):
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

    def test_post_actors_by_casting_assistant_without_auth(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}".format(self.casting_assistant)
                                      },
                                      json={
                                          "name": "Edward",
                                          "gender": "male",
                                          "age": 25,
                                      })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        
        

    def test_post_movies_by_executive_producer_with_auth(self):
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


    def test_post_movies_by_casting_assistant_without_auth(self):
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



    def test_get_actors_by_casting_assistant_with_auth(self):
        response = self.client().get('/actors',
                                     headers={
                                         "Authorization": "Bearer {}".format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_get_actors_by_casting_assistant_without_auth(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')




    def test_get_movies_by_casting_assistant_with_auth(self):
        response = self.client().get('/movies',
                                     headers={
                                         "Authorization": "Bearer {}".format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_get_movies_by_casting_assistant_without_auth(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')


    def test_patch_actors_by_executive_producer_200(self):
        random_id = random.choice([ actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.executive_producer)
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

    def test_patch_actors_by_executive_producer_404(self):
        id = 999
        response = self.client().patch('/actors/{}'.format(id),
                                       headers={
            "Authorization": "Bearer {}".format(self.executive_producer)
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


    def test_patch_movies_by_executive_producer_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.executive_producer)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    
    def test_patch_movies_by_executive_producer_404(self):
        id = 999
        response = self.client().patch('/movies/{}'.format(id),
                                       headers={
            "Authorization": "Bearer {}".format(self.executive_producer)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status_message'], "resource Not found")


    def test_delete_actors_by_executive_producer_200(self):
        random_id = random.choice([ actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_delete_actors_by_executive_producer_404(self):
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

    def test_delete_movies_by_executive_producer_200(self):
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

    def test_delete_movies_by_executive_producer_404(self):
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
