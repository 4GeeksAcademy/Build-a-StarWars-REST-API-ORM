"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import People
from models import Planets
from models import Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people(): 
    people = User.query.all()
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people = People.query.get(people_id)
    return jsonify(people), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify(planet), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_fav():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites = Favorites.query.filter_by(user_id=user_id).all()

    fav_list = [
        {"planet": Planets.query.get(fav.planet_id).name} if fav.planet_id else
        {"people": People.query.get(fav.people_id).name}
        for fav in favorites
    ]
    return jsonify(fav_list if fav_list else {"message": "No favorites found"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_fav(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 400
    
    fav_registrado = Favorites.query.filter_by(planet_id=id).first()
    if fav_registrado:
        return jsonify ({"error": "The planet is already on the favorites list"})
    new_fav = Favorites(planet_id=id)

    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": f"The planet {planet.name} has been added to your favorites"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_fav(people_id):
    people = People.query.get(people_id)
    if not people:
        return jsonify({"error": "People not found"}), 400
    
    fav_registrado = Favorites.query.filter_by(people_id=id).first()
    if fav_registrado:
        return jsonify ({"error": "The people is already on the favorites list"})
    new_fav = Favorites(people_id=id)

    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": f"The people {people.name} has been added to your favorites"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    people = People.query.get(people_id)
    db.session.delete(people)
    db.session.commit()

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
