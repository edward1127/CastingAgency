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
        self.casting_assistant = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjZDFmNTg3M2JhMzYwZWQzYTZiMGVhIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTI2MDgwOCwiZXhwIjoxNTc1MzMyODA4LCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.f8OfeZ3uvBas-X6cpZsn2zo7bFboSyFIBTJDxP1vegnw7gDa0wbRtb_AZPxGl2LTDdY-U3SX0gT3hYfZySdOYvhpYlxp-HqGOsJ7Ra3ZhidpC-9_lm_QKJyKna3vJ6GheHP2UKoqq6cyDC7h1ju3OTAGxMVIgPE960Gl9OQ9r0EgVQ35k82qi1qEQplM24wwWX7eFOLpAsmxeLCBohzrfHs3C1ImdujCZJaVpllEbnWyIZ4hp4s_fIhrnUcElfJmjumCRGhFy4KLNTRlZk9TuhKZfq2X8Zeruhx1ZerVabeSvv4GTNpY4ywyyzkPH13GkdGxBzi3Ru0U8HWV7BU5sg'
        self.casting_director = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkMDkxNmFiZmIyOGMwZWNiYTVkNDljIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTI0MzQ5MSwiZXhwIjoxNTc1MzE1NDkxLCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.efQZegjY_DL_HZ3dh-aBfolUMB6HhdwcosX21V0Uhy9T73DbLt8EIPEJtIKsKygZ5u1bxVDGRI2WZmwMGbn1eOs2otgImRA6bZA7kjoeNAcGiElsKecu6BXfUNEuT4hkMy--XYF-fKFRaO0LD5riIiZNV2NPgvqqHmfb3EKqA6lyfqAzus9gbRyTkS3jfor_06SlIZx87wTwM9sZbMc51p0uo3Tja04xgTPZxQi8gY2GkNb_nWX2mqtD8sv-RilnMkBH31oxrHmVw9oTh0hHmwnDbhGpcrOxAj54gtX2RJo7s6CInk-Rokleg7_QAgyak45dCrBEpmBDJwfcK4agdA'
        self.executive_producer = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlMjAyNDY2OGJhZTEwZDJhN2MwNDVlIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTI2MDg4OSwiZXhwIjoxNTc1MzMyODg5LCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.xbj7v8yMgZwco2jtsvn3J7lRJjAsiwCyrSRdRdcRuUEJXq9yExL1sd5DSrr8eCAGuOZXmM8QJJvrdPEcnMMXPMe519OqypCBHhiYKva8erihK2dhqLaPzSU5OrDA9i8vfcI0uIUlTGrrTlYDyxo7q1VHSJUk0-oIrggOHCymqcno39hSoZtZXGSiC7SlTUNwdETerYXVWqm9Rzp9Xq3jkTpDXlyjyeLzvhh4BeGLwhN0vSpQwtCUcNU9UNnqadjbU64XptuLk9NZEn9vabyZmMertqMxo2hRd6CDtfRRgIfN3k3wdLQx8cDh8P2qag8osfeI3QCukk0QCLXNIx5I_w'
        setup_db(self.app, TEST_DATABASE_URI)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


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
                                          "age": 25
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

    def test_patch_actors_by_casting_director_200(self):
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

    def test_patch_actors_by_casting_director_404(self):
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

    def test_patch_movies_by_casting_director_200(self):
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

    def test_patch_movies_by_casting_director_404(self):
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

    def test_delete_actors_by_executive_producer_200(self):
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
