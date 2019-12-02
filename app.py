import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db, setup_db, Actor, Movie, movies



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    

    @app.route('/actors')
    @requires_auth('view:actors')
    def get_actors():
        actors = [actor.attributes()
                  for actor in Actor.query.order_by(Actor.id).all()]
        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "actors": actors
        })

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS'
        )
        return response

    @app.route('/movies')
    @requires_auth('view:movies')
    def get_movies():
        movies = [movie.attributes()
                  for movie in Movie.query.order_by(Movie.id).all()]
        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movies": movies
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actors(id):
        target_actor = Actor.query.filter(Actor.id == id).one_or_none()
        if target_actor is None:
            abort(404)
        target_actor.delete()

        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": id})

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(id):
        target_movie = Movie.query.filter(Movie.id == id).one_or_none()
        if target_movie is None:
            abort(404)
        target_movie.delete()

        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": id})

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='add:actors')
    def post_actors():

        name = request.json.get("name", None)
        age = request.json.get("age", None)
        gender = request.json.get("gender", None)

        if name is None:
            abort(422)

        new_actor = Actor(name=name, age=age, gender=gender)
        new_actor.insert()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": "OK",
            "actor": new_actor.attributes()
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='add:movies')
    def post_movies():

        title = request.json.get("title", None)
        release_date = request.json.get("release_date", None)

        if title is None:
            abort(422)

        new_movie = Movie(title=title, release_date=release_date)
        new_movie.insert()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movie": new_movie.attributes()
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='edit:actors')
    def patch_actors(id):
        name = request.json.get("name", None)
        age = title = request.json.get("age", None)
        gender = title = request.json.get("gender", None)
        target_actor = Actor.query.filter(Actor.id == id).one_or_none()
        if target_actor is None:
            abort(404)
        if name is None:
            abort(422)

        target_actor.name = name
        target_actor.age = age
        target_actor.gender = gender
        target_actor.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "actor": target_actor.attributes()
        })

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='edit:movies')
    def patch_movies(id):
        title = request.json.get("title", None)
        release_date = request.json.get("release_date", None)
        target_movie = Movie.query.filter(Movie.id == id).one_or_none()

        if target_movie is None:
            abort(404)

        if title is None:
            abort(422)

        target_movie.title = title
        target_movie.release_date = release_date
        target_movie.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movie": target_movie.attributes()
        })

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "status_message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "status_message": "resource Not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
