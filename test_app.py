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
        self.casting_assistant = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlNThhYmYyY2UwYjcwZDJhOTQ1NjNlIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTMzNDQ2NiwiZXhwIjoxNTc1NDA2NDY2LCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.s2CSKLYmwg4cW2u7Q9XmYFpd5TyrK0jZohFN3AUGSl0AD1nMsycImMYB3k2m2i5HVVuzaFTfwsHtPHWDiXbd28IJ4LTcxhV7GSGtne_zYfDVh7Vz_FFjclx21U5475yBOg1TbiyipkMFL81c7dIL-tU5-z1TNAzWlv6RXQDyOyX_q0lnh9Xd9R0uvnSAMuYM5Io0n3WzvzTTtR_2xlyXBcc8TfaNYDDzXJdrCC7yLXHWwyrsLaw9tyQrMlikFdnP9HSJZ1jpA1sGQg86PQ6-ug0j2QpNoNqpFWSGcQQ1Pvdn-lvgksGodlbeNg8xX1zhVXfsDHuaRR62rkBNN9iB5w'
        self.casting_director = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlNThiM2Q4NDFlZTkwZDMwZGFmYWFkIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTMzNDU0OCwiZXhwIjoxNTc1NDA2NTQ4LCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.av_ddAORfg-7rkQJgsn001j1vF7L_-umxKnr2u8KUxHj-Fu2escc2lnZ_yBCMJ0MTuPpOoRnu4qyyU-7w39qcOYwu9RPnzKxwdDCMF7coePhl97NfIX734IXplKj1PGLam4B-2gK1TEzUAj8_VrQYM5KiiKc-DCTzVtFT0muFi0aiR2z18Gjq3-H3-5fJjBxhKNgMqcxSv5v370-E9ePx8waji2T81GdVk8H5nJ_28msHXtfOl6LI0GRF6SEserRQt_5jRz8fxfokGSPaxhBLDT-E_f_ryPNT4Tu7qUrqlvcTn6GqexH3BqPkR7NPVqQvEvUAkZXRCzFcuWpkZT3rw'
        self.executive_producer = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUVkJOREV5T0RNMk1USXlNRE0wT1VJd1JFUXlOakF3TmpVd01qWTBRalF6UTBORE0wVkJPUSJ9.eyJpc3MiOiJodHRwczovL2NoZWVybW9vbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlNWFjMmIyY2UwYjcwZDJhOTQ1NzhjIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU3NTMzNDYxNSwiZXhwIjoxNTc1NDA2NjE1LCJhenAiOiIwQWNsV1BXRndVbjFyWjB1cTIyVUt5b2w1Q1YwMUdTTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.ehQMoI-Qwv26JyvMhEaSdI7CNTewHVMyUhK-mpDguWBcLhRGd5Or0k2tcEEqiY6009klb3yOQuc185ajTtu__7GAu9RRXudbDF-9kKCcgoJWrwyT-Qpa9SgPQg9VF-nLYAlK6Gz-QHRCegRRMVeorjC5dsFwfiiCLdVqUig_F5xxjGUskGlqN1h2jAOVMVaH6rPOp4rG4YGRxM9ATEViwXmzNe8JBWfOmk2CVEk0wK0ceqLHMuz8W0U8SOkbKI4yoX56fzTl_cDooxLJxlptC9vpK2PWFe84c1wPsxpX118wWpOBnOSGwEUA78KsyhCr8kq5md0zbdFyFSAxR_oJeQ'
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
